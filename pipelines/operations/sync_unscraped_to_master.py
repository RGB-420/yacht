import pandas as pd

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

from app.core.config import DATA_MASTER, DATA_QUEUE

MASTER_PATH = DATA_MASTER / "regattas_master.csv"

UNSCRAPED_PATH = DATA_QUEUE / "unscraped_regattas.csv"

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
        (
            row["regatta_name"],
            str(row["year"]),
            row["link"]
            if pd.notna(row["link"])
            else ""
        ): row

        for _, row in unscraped_df.iterrows()
    }

    updated = 0

    for idx, row in master_df.iterrows():
        key = (
            row["regatta_name"],
            str(row["year"]),
            row["link"]
            if pd.notna(row["link"])
            else ""
        )

        unscraped_row = unscraped_index.get(key)

        if unscraped_row is None:
            continue

        master_df.at[
            idx,
            "scrape_active"
        ] = unscraped_row["scrape_active"]

        updated += 1

    master_df.to_csv(MASTER_PATH, index=False)

    logger.info(f"Rows synced from unscraped: {updated}")
