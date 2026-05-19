import pandas as pd

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

from app.core.config import DATA_MASTER

MASTER_PATH = DATA_MASTER / "regattas_master.csv"

def update_scrape_status(regatta_name, year, link):
    logger.info(f"Updating scrape status: {regatta_name} ({year})")

    df = pd.read_csv(MASTER_PATH)

    for col in df.columns:
        df[col] = df[col].astype("string").str.strip()

    df = df.replace(r"^\s*$", pd.NA, regex=True)

    updated = False

    for idx, row in df.iterrows():
        row_link = (
            row["link"]
            if pd.notna(row["link"])
            else ""
        )

        target_link = (
            link
            if pd.notna(link)
            else ""
        )

        if (
            row["regatta_name"] == regatta_name
            and str(row["year"]) == str(year)
            and row_link == target_link
        ):
            df.at[idx, "scrape_active"] = 0

            df.at[idx, "scrape_status"] = "Scrapeado"

            updated = True

            break
    
    if updated:
        df.to_csv(MASTER_PATH, index=False)

        logger.info("Scrape status updated")

    else:
        logger.warning("Regatta not found in master")