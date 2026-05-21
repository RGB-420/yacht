import pandas as pd

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

from app.core.config import DATA_MASTER, DATA_QUEUE

MASTER_PATH = DATA_MASTER / "regattas_master.csv"

UNSCRAPED_PATH = DATA_QUEUE / "unscraped_regattas.csv"

SYNC_COLUMNS = [
    "status",
    "scraper_name",
    "source_type",
    "scrape_active",
    "scrape_status",
    "specified_class",
    "start_date",
    "end_date",
    "notes",
    "link"
]

def sync_unscraped_to_master():
    logger.info("Syncing unscraped regattas to master...")

    master_df = pd.read_csv(MASTER_PATH)

    unscraped_df = pd.read_csv(UNSCRAPED_PATH)

    for df in [master_df, unscraped_df]:
        for col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    master_df = master_df.replace(r"^\s*$", pd.NA, regex=True)

    unscraped_df = unscraped_df.replace(r"^\s*$", pd.NA, regex=True)

    unscraped_index = {
        row["source_id"]: row
        for _, row in unscraped_df.iterrows()
    }

    updated = 0

    for idx, row in master_df.iterrows():
        key = row["source_id"]

        unscraped_row = unscraped_index.get(key)

        if unscraped_row is None:
            continue

        for col in SYNC_COLUMNS:
            if col not in unscraped_row:
                continue

            master_df.at[idx, col] = unscraped_row[col]

        updated += 1

    master_df.to_csv(MASTER_PATH, index=False)

    logger.info(f"Rows synced from unscraped: {updated}")
