import pandas as pd

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

from app.core.config import DATA_MASTER

MASTER_PATH = DATA_MASTER / "regattas_master.csv"

def update_scrape_status(source_id):
    logger.info(f"Updating scrape status: {source_id})")

    df = pd.read_csv(MASTER_PATH)

    for col in df.columns:
        df[col] = df[col].astype("string").str.strip()

    df = df.replace(r"^\s*$", pd.NA, regex=True)

    updated = False

    for idx, row in df.iterrows():
        if row["source_id"] == source_id:
            df.at[idx, "scrape_active"] = "0"

            df.at[idx, "scrape_status"] = "Scrapeado"

            updated = True

            break
    
    if updated:
        df.to_csv(MASTER_PATH, index=False)

        logger.info("Scrape status updated")

    else:
        logger.warning("Regatta not found in master")