import pandas as pd

from app.core.config import DATA_MAPPING

from app.repositories.class_types_repo import bulk_upsert_class_types, load_class_type_cache

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

RESOLVED_PATH = DATA_MAPPING / "class_types/class_type_resolved.csv"

def sync_class_types(conn):
    logger.info("Syncing class types...")

    df = pd.read_csv(RESOLVED_PATH)

    logger.info(f"Rows loaded: {len(df)}")

    for col in df.columns:
        df[col] = df[col].astype("string").str.strip()

    df = df.replace(r"^\s*$", pd.NA, regex=True)

    class_types_df = df[(df["status"] == "resolved") & (df["canonical_class"].notna() | df["canonical_type"].notna())]

    class_types_df = class_types_df[["canonical_class", "canonical_type"]].drop_duplicates().reset_index(drop=True)

    existing_cache = load_class_type_cache(conn)

    logger.info(f"Existing class types: {len(existing_cache)}")

    payload = []

    for row in class_types_df.itertuples(index=False):
        key = (str(row.canonical_class).upper() if pd.notna(row.canonical_class) else None, str(row.canonical_type).upper() if pd.notna(row.canonical_type) else None)

        if key in existing_cache:
            continue

        payload.append({"canonical_class": (None if pd.isna(row.canonical_class) else row.canonical_class), "canonical_type": (None if pd.isna(row.canonical_type) else row.canonical_type)})

    if payload:
        bulk_upsert_class_types(conn, payload)

    logger.info(f"Class types synced: {len(payload)}")
