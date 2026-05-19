import pandas as pd

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

from app.core.config import DATA_MASTER, DATA_QUEUE

MASTER_PATH = DATA_MASTER / "regattas_master.csv"

UNSCRAPED_PATH = DATA_QUEUE / "unscraped_regattas.csv"

def generate_unscraped_regattas():
    logger.info("Generating unscraped regattas...")

    df = pd.read_csv(MASTER_PATH)

    for col in df.columns:
        df[col] = df[col].astype("string").str.strip()

    df = df.replace(r"^\s*$", pd.NA, regex=True)

    unscraped_df = df[df["scrape_status"].fillna("") != "Scrapeado"].copy()

    unscraped_df = (unscraped_df.sort_values(by=["scrape_active", "start_date", "end_date"], ascending=[False, True, True]).reset_index(drop=True))

    unscraped_df.to_csv(UNSCRAPED_PATH, index=False)

    logger.info(f"Unscraped regattas exported: {len(unscraped_df)}")
