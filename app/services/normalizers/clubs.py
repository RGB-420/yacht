import pandas as pd
import re 

from pathlib import Path

from app.services.mappings.club_mapping import club_mapping
from app.core.config import DATA_PRENORM

"""
Club normalizer

⚠️ Depends on 'Name' column for inference
"""

PRENORM_PATH = DATA_PRENORM / "club_prenormalization.csv"
SEEN_PRENORM = set()

# ------ Main function ------
def finalize_club_column(df):
    if "Club"  not in df.columns:
        return df
    
    df["Club"] = df["Club"].apply(split_club)
    df = df.explode("Club").reset_index(drop=True)

    df["Club"] = df.apply(
        lambda row: infer_club_from_boat_name(row["Name"], row.get("Club")),
        axis=1
    )

    # Guardar raw
    df["Club_raw"] = df["Club"]

    # Normalizar
    df["Club_norm"] = (
        df["Club"]
        .apply(normalize_club)
        .astype("string")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Mapear o capturar prenormalization
    df["Club"] = df.apply(
        lambda row: map_or_collect_club(row["Club_norm"], row["Club_raw"]),
        axis=1
    )

    df = df.drop(columns=["Club_raw", "Club_norm"])

    return df


# ------ Utils ------
INFER_PATTERNS = {
    r"\bRTYC\b": "Royal Thames Yacht Club",
    r"\bROYAL\s+THAMES\b": "Royal Thames Yacht Club",
}

def normalize_club(s):
    if pd.isna(s):
        return None

    s = str(s).upper()

    # Normalizar unicode raro
    s = re.sub(r"[‐-‒–—―]", "-", s)

    # Quitar puntuación excepto espacios
    s = re.sub(r"[^\w\s]", " ", s)

    # Normalizar siglas completas
    s = re.sub(r"\bYACHT\s*CLUB\b", "YACHT CLUB", s)
    s = re.sub(r"\bSAILING\s*CLUB\b", "SAILING CLUB", s)

    # Espacios
    s = re.sub(r"\s+", " ", s).strip()

    return s

def map_or_collect_club(norm_name, raw_name):
    if pd.isna(norm_name):
        return None

    raw_name = str(raw_name).strip().upper()
    norm_name = str(norm_name).strip().upper()

    entry = club_mapping.get(raw_name)

    if entry is not None:
        if entry["status"] == "resolved":
            return entry["canonical"]
        else:
            return None
        
    entry = club_mapping.get(norm_name)

    if entry is not None:
        if entry["status"] == "resolved":
            return entry["canonical"]
        else:
            return None

    save_club_prenorm(norm_name)

    return None

def split_club(cell):
    if pd.isna(cell):
        return []

    # 1) Split por separadores habituales
    parts = re.split(r"\s*/\s*|\s*&\s*|\band\b|,\s*", cell, flags=re.IGNORECASE)
    parts = [p.strip() for p in parts if p.strip()]
    return list(dict.fromkeys(parts))

def infer_club_from_boat_name(name, club):
    if pd.isna(name):
        return club

    if not (pd.isna(club) or str(club).strip() == ""):
        return club

    name_str = str(name)

    for pattern, club_name in INFER_PATTERNS.items():
        if re.search(pattern, name_str, re.IGNORECASE):
            return club_name

    return club

def save_club_prenorm(norm_name):
    if pd.isna(norm_name) or str(norm_name).strip() == "":
        return

    if norm_name in SEEN_PRENORM:
        return

    SEEN_PRENORM.add(norm_name)

    row = {
        "club_raw_name": norm_name,
        "club_canonical_name": "",
        "status": "pending",
        "confidence": "",
        "notes": ""
    }

    df_new = pd.DataFrame([row])

    if PRENORM_PATH.exists():
        df_new.to_csv(PRENORM_PATH, mode="a", header=False, index=False)
    else:
        df_new.to_csv(PRENORM_PATH, index=False)