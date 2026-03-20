import pandas as pd
import re 

from pathlib import Path

from domain.mappings.club_mapping import club_mapping

"""
Club normalizer

⚠️ Depends on 'Name' column for inference
"""

PRENORM_PATH = Path("domain/mappings/club_prenormalization.csv")
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

    canonical = club_mapping.get(norm_name)

    if canonical:
        return canonical

    save_club_prenorm(raw_name)

    return raw_name

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

def save_club_prenorm(raw_name):
    if pd.isna(raw_name) or str(raw_name).strip() == "":
        return

    key = str(raw_name).lower()

    if key in SEEN_PRENORM:
        return

    SEEN_PRENORM.add(key)

    row = {
        "raw_name": raw_name,
        "canonical_name": "",
        "status": "pending",
        "confidence": "",
        "notes": ""
    }

    df_new = pd.DataFrame([row])

    if PRENORM_PATH.exists():
        df_existing = pd.read_csv(PRENORM_PATH)

        if key in df_existing["raw_name"].str.lower().values:
            return

        df_final = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_final = df_new

    df_final.to_csv(PRENORM_PATH, index=False)