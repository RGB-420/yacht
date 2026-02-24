import re
import pandas as pd
import unicodedata

from domain.mappings.owner_mapping import owner_mapping

"""
Owner normalizer

⚠️ This module may modify the 'Club' column when owner and club
are combined in the same cell (e.g. "John Smith - Royal Thames YC").
"""

# ------ Main function ------
def finalize_owner_column(df):
    if "Owner" not in df.columns:
        return df

    df["Owner"] = df["Owner"].str.lower()
    df["Owner"] = df["Owner"].apply(split_and_dedupe)
    df = df.explode("Owner").reset_index(drop=True)

    df["Owner"] = (df["Owner"].astype("string").str.replace(r"\s+", " ", regex=True).str.strip())

    df["Owner"] = df["Owner"].apply(map_owner)

    df[["Owner", "Club"]] = df.apply(
        lambda row: pd.Series(
            split_owner_and_club(row["Owner"], row.get("Club"))
        ),
        axis=1
    )
    
    df["Owner"] = df["Owner"].str.title()

    return df

# ------ Utils ------
def normalize_owner(name):
    if pd.isna(name):
        return None

    name = str(name)

    # Normalizar unicode (quita caracteres raros)
    name = unicodedata.normalize("NFKD", name)

    # Unificar guiones
    name = re.sub(r"[‐-‒–—―]", "-", name)

    # Minúsculas
    name = name.lower()

    # Quitar puntuación
    name = re.sub(r"[.,]", "", name)

    # Espacios múltiples
    name = re.sub(r"\s+", " ", name)

    return name.strip()

def map_owner(name):
    norm = normalize_owner(name)
    return owner_mapping.get(norm, name)

def split_and_dedupe(cell):
    if pd.isna(cell):
        return cell
    
    cell = cell.replace("|", "/")

    # 1) Split por separadores habituales
    parts = re.split(r"\s*/\s*|\s*&\s*|\s+and\s+|,\s*|\s+en\s+", cell)
    parts = [p.strip() for p in parts if p.strip()]

    # 2) Detectar apellido común
    surnames = []
    for p in parts:
        tokens = p.split()
        if len(tokens) > 1:
            surnames.append(tokens[-1])

    common_surname = surnames[-1] if surnames else None

    # 3) Heredar apellido si falta
    fixed = []
    for p in parts:
        if len(p.split()) == 1 and common_surname:
            fixed.append(f"{p} {common_surname}")
        else:
            fixed.append(p)

    # 4) Quitar duplicados manteniendo orden
    return list(dict.fromkeys(fixed))

def split_owner_and_club(owner, club):
    if pd.isna(owner):
        return owner, club

    owner_str = str(owner).strip()

    parts = re.split(r"\s*[-–—]\s*", owner_str)

    if len(parts) > 1:
        owner_part = None
        club_part = None

        for p in parts:
            if re.search(r"\b(yacht club|rdyc|rtyc|llyc|sailing club|\bclub\b)", p, re.IGNORECASE):
                club_part = p.strip()
            else:
                owner_part = p.strip()

        if owner_part and club_part:
            if pd.isna(club) or str(club).strip() == "":
                club = club_part
            owner = owner_part
            return owner, club

    if (
        re.search(r"\b(yacht club|rdyc|rtyc|llyc|sailing club|\bclub\b)", owner_str, re.IGNORECASE)
        and (pd.isna(club) or str(club).strip() == "")
    ):
        return pd.NA, owner_str

    return owner, club