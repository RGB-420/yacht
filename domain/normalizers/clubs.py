import pandas as pd
import re 

from domain.mappings.club_mapping import club_mapping

"""
Club normalizer

⚠️ Depends on 'Name' column for inference
"""

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

    df["Club"] = (
        df["Club"]
        .apply(normalize_club)
        .astype("string")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    #df["Club"] = df["Club_norm"].apply(map_club)
    return df
"""    mask = df["Club_canonical"].isna()

    df.loc[mask, "Club_canonical"] = (
        df.loc[mask, "Club_norm"]
        .str.replace(r"\s*y\s*c\.?\s*$", " yacht club", regex=True, case=False)
        .str.replace(r"\s*s\s*c\.?\s*$", " sailing club", regex=True, case=False)
    )

    df["Club"] = df["Club_canonical"].fillna(df["Club_norm"].str.title())"""
    


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

def map_club(norm_name):
    if pd.isna(norm_name):
        return None
    return club_mapping.get(norm_name, None)

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
