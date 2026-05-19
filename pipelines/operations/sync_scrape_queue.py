import pandas as pd

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

from app.core.config import DATA_MASTER, DATA_QUEUE

QUEUE_PATH = DATA_QUEUE / "scrape_queue.csv"

MASTER_PATH = DATA_MASTER / "regattas_master.csv"

def sync_scrape_queue():
    logger.info("Syncing scrape queue to master...")

    master_df = pd.read_csv(MASTER_PATH)

    queue_df = pd.read_csv(QUEUE_PATH)

    for df in [master_df, queue_df]:
        for col in df.columns:
            df[col] = (df[col].astype("string").str.strip())

    master_df = master_df.replace(r"^\s*$", pd.NA, regex=True)

    queue_df = queue_df.replace(r"^\s*$", pd.NA, regex=True)

    logger.info(f"Master rows: {len(master_df)}")

    logger.info(f"Queue rows: {len(queue_df)}")

    master_index = set(
        zip(
            master_df["regatta_name"].fillna(""),
            master_df["year"].astype(str),
            master_df["link"].fillna("")
        )
    )

    new_rows = []

    for _, row in queue_df.iterrows():
        key = (
            row["regatta_name"],
            str(row["year"]),
            row["link"] if pd.notna(row["Link"]) else ""
        )

        if key not in master_index:
            new_rows.append(row)

    if new_rows:
        new_df = pd.DataFrame(new_rows)

        master_df = pd.concat(
            [master_df, new_df],
            ignore_index=True
        )

        logger.info(f"New regattas added: {len(new_df)}")

    master_df.to_csv(MASTER_PATH, index=False)

    queue_df.iloc[0:0].to_csv(
        QUEUE_PATH,
        index=False
    )

    logger.info("Scrape queue synced successfully")