import pandas as pd

from app.core.config import DATA_MAPPING

from app.repositories.class_type_aliases_repo import bulk_upsert_class_type_aliases, load_class_type_alias_cache
from app.repositories.class_types_repo import load_class_type_cache
from app.repositories.class_type_alias_relations_repo import load_class_type_alias_relations_cache, bulk_insert_class_type_alias_relations

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

RESOLVED_PATH = DATA_MAPPING / "class_types/class_type_resolved.csv"

def sync_class_type_mapping(conn):
    logger.info("Syncing class type mappings...")

    df = pd.read_csv(RESOLVED_PATH)

    logger.info(f"Rows loaded: {len(df)}")

    for col in df.columns:
        df[col] = df[col].astype("string").str.strip()

    df = df.replace(r"^\s*$", pd.NA, regex=True)

    df = df[(df["status"] == "resolved") & (df["canonical_class"].notna() | df["canonical_type"].notna())].copy()

    alias_payload = []

    for row in df.itertuples(index=False):
        alias_payload.append({
            "raw_class": None if pd.isna(row.raw_class) else row.raw_class,
            "raw_type": None if pd.isna(row.raw_type) else row.raw_type,
            "normalized_class": None if pd.isna(row.raw_class) else row.raw_class,
            "normalized_type": None if pd.isna(row.raw_type) else row.raw_type,
            "status": row.status,
            "confidence": None if pd.isna(row.confidence) else row.confidence
        })
    
    if alias_payload:
        bulk_upsert_class_type_aliases(conn, alias_payload)

    logger.info(f"Aliases synced: {len(alias_payload)}")

    raw_alias_cache, normalized_alias_cache = load_class_type_alias_cache(conn)

    logger.info(f"Raw alias cache: {len(raw_alias_cache)}")
    logger.info(f"Normalized alias cache: {len(normalized_alias_cache)}")

    class_type_cache = load_class_type_cache(conn)

    relation_cache = load_class_type_alias_relations_cache(conn)

    logger.info(f"Class type cache: {len(class_type_cache)}")
    logger.info(f"Relation cache: {len(relation_cache)}")

    relations_payload = []

    for row in df.itertuples(index=False):
        alias_key = (
            str(row.raw_class).upper()
            if pd.notna(row.raw_class)
            else None,

            str(row.raw_type).upper()
            if pd.notna(row.raw_type)
            else None
        )

        alias = (raw_alias_cache.get(alias_key) or normalized_alias_cache.get(alias_key))

        if not alias:
            continue

        class_type_key = (str(row.canonical_class).upper() if pd.notna(row.canonical_class) else None, str(row.canonical_type).upper() if pd.notna(row.canonical_type) else None)

        id_class_type = class_type_cache.get(class_type_key)

        if not id_class_type:
            continue

        relation_key = (alias["id_alias"], id_class_type)

        if relation_key in relation_cache:
            continue

        relations_payload.append({
            "id_alias": alias["id_alias"],
            "id_class_type": id_class_type
        })
    
    if relations_payload:
        bulk_insert_class_type_alias_relations(conn, relations_payload)
    
    logger.info(f"Relations synced: {len(relations_payload)}")
