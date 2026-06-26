import pandas as pd

from app.core.config import DATA_PRENORM, DATA_MAPPING

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

PRENORM_PATH = DATA_PRENORM / "owner_prenormalization.csv"
MAPPING_PATH = DATA_MAPPING / "owner_mapping.csv"

def sync_owner_mapping():
    logger.info("Syncing owner mapping...")

    if not PRENORM_PATH.exists():
        logger.warning("owner_prenormalization.csv not found")
        return
    
    prenorm_df = pd.read_csv(PRENORM_PATH)

    logger.info(f"Prenorm rows: {len(prenorm_df)}")

    if MAPPING_PATH.exists():
        mapping_df = pd.read_csv(MAPPING_PATH)

    else:
        mapping_df = pd.DataFrame(columns=["raw_name", "canonical_name"])

    resolved_df = prenorm_df[prenorm_df["status"] == "resolved"].copy()

    logger.info(f"Resolved rows: {len(resolved_df)}")

    new_rows = resolved_df[~resolved_df["raw_name"].isin(mapping_df["raw_name"])][["raw_name", "canonical_name", "confidence", "notes"]]

    logger.info(f"New mappings: {len(new_rows)}")

    if not new_rows.empty:
        mapping_df = pd.concat([mapping_df, new_rows], ignore_index=True)

        mapping_df = mapping_df.sort_values(by=["raw_name"]).reset_index(drop=True)

        mapping_df.to_csv(MAPPING_PATH, index=False)

        logger.info(f"Owner mapping updated: {MAPPING_PATH}")

    else:
        logger.info("No new owner mapping found")        