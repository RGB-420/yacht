import re
import pandas as pd
import unicodedata

from pathlib import Path

from app.services.mappings.owner_mapping import owner_mapping

from app.services.automapping.owners import automap_owner

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

"""
Owner normalizer

⚠️ This module may modify the 'Club' column when owner and club
are combined in the same cell (e.g. "John Smith - Royal Thames YC").
"""

PRENORM_PATH = Path("data/prenormalization/owner_prenormalization.csv")

SEEN_PRENORM = set()

EXISTING_PRENORM = set()

PRENORM_ROWS = []

DEBUG_PATH = Path("data/debug/owner_raw_debug.csv")

DEBUG_ROWS = []

# ------ Main function ------
def finalize_owner_column(df):
    df = df.copy()
    
    if "Owner" not in df.columns:
        return df
    
    for _, row in df.iterrows():
        save_owner_debug(row["Owner"], row["Source"])

    df.loc[:, "Owner"] = df["Owner"].apply(split_and_dedupe)
    df = df.explode("Owner").reset_index(drop=True)

    df["Owner"] = (df["Owner"].astype("string").str.replace(r"\s+", " ", regex=True).str.strip())

    df[["Owner", "Club"]] = df.apply(
        lambda row: pd.Series(
            split_owner_and_club(row["Owner"], row.get("Club"))
        ),
        axis=1
    )

    # Normalizar
    df["Owner_norm"] = df["Owner"].apply(normalize_owner).astype("string")

    # Mapear o capturar prenormalization
    df["Owner"] = df.apply(
        lambda row: map_or_collect_owner(row["Owner_norm"], row["Owner"]),
        axis=1
    )
    
    df["Owner"] = df["Owner"].str.title()

    df = df.drop(columns=["Owner_norm"])

    flush_owner_prenorm(rebuild=True)
    flush_owner_debug()

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

def map_or_collect_owner(norm_name, raw_name):
    if pd.isna(norm_name):
        return None

    canonical = owner_mapping.get(norm_name)

    if canonical:
        return canonical

    # no mapeado → guardar
    save_owner_prenorm(raw_name)

    return str(raw_name).strip()

def split_and_dedupe(cell):
    if pd.isna(cell):
        return cell
    
    cell = str(cell)

    cell = re.sub(r"\s+", " ", cell).strip()
    cell = cell.replace("|", "/")

    # Split por separadores habituales
    parts = re.split(r"\s*/\s*|\s*&\s*|\s+and\s+|\s+et\s+|,\s*|\s+en\s+", cell, flags=re.IGNORECASE)
    parts = [p.strip() for p in parts if p.strip()]

    if len(parts) > 4:
        logger.warning(f"Suspicious owner split: {cell}")


    # Detectar apellido común
    surnames = []

    for p in parts:
        tokens = p.split()

        if len(tokens) > 1:
            surnames.append(tokens[-1])

    common_surname = surnames[-1] if surnames else None

    # Heredar apellido si falta
    fixed = []

    for p in parts:
        if len(p.split()) == 1 and common_surname and p.lower() not in {"son", "family", "friends", "associates"}:
            fixed.append(f"{p} {common_surname}")
        else:
            fixed.append(p)

    # Quitar duplicados manteniendo orden
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
            logger.warning(
                f"Moved owner -> club: {owner_str}"
            )

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

def save_owner_prenorm(raw_name):
    if pd.isna(raw_name) or str(raw_name).strip() == "":
        return

    key = str(raw_name).lower()

    if key in SEEN_PRENORM:
        return
    
    if key in EXISTING_PRENORM:
        return
    
    SEEN_PRENORM.add(key)
    EXISTING_PRENORM.add(key)

    classification = automap_owner(raw_name)

    PRENORM_ROWS.append({
        "raw_name": raw_name,
        "canonical_name": classification["canonical_name"],
        "status": "pending",
        "confidence": classification["confidence"],
        "entity_type": classification["entity_type"],
        "notes": classification["notes"]
    })

def flush_owner_prenorm(rebuild=False):
    if not PRENORM_ROWS:
        return
    
    df_new = pd.DataFrame(PRENORM_ROWS)

    if PRENORM_PATH.exists() and not rebuild:
        df_existing = pd.read_csv(PRENORM_PATH)

        df_final = pd.concat([df_existing, df_new], ignore_index=True)
    
    else:
        df_final = df_new

    df_final = df_final.sort_values(by=["notes", "confidence", "raw_name"], ascending=[True, False, True], na_position="last").reset_index(drop=True)

    df_final.to_csv(PRENORM_PATH, index=False)

    logger.info(f"Owner prenorm saved: {len(PRENORM_ROWS)} rows")

    PRENORM_ROWS.clear()

def save_owner_debug(raw_owner, source):
    if pd.isna(raw_owner):
        return
    
    raw_owner = str(raw_owner).strip()

    if not raw_owner:
        return
    
    DEBUG_ROWS.append({
        "raw_owner": raw_owner,
        "source": source,
        "owner_count": len(split_and_dedupe(raw_owner))
    })

def flush_owner_debug():
    if not DEBUG_ROWS:
        return
    
    df = pd.DataFrame(DEBUG_ROWS)

    df = df.drop_duplicates()

    if DEBUG_PATH.exists():
        existing = pd.read_csv(DEBUG_PATH)

        df = pd.concat([existing, df], ignore_index=True)

        df = df.drop_duplicates(subset=["raw_owner", "source"])

    df = df.sort_values(by=["raw_owner"]).reset_index(drop=True)

    df.to_csv(DEBUG_PATH, index=False)

    logger.info(f"Owner debug saved: {len(df)} rows")
