import pandas as pd
import re

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

from app.core.config import DATA_MASTER, DATA_QUEUE

QUEUE_PATH = DATA_QUEUE / "scrape_queue.csv"

MASTER_PATH = DATA_MASTER / "regattas_master.csv"

def sync_scrape_queue():
    logger.info("Syncing scrape queue to master...")

    master_df = pd.read_csv(MASTER_PATH)

    queue_df = pd.read_csv(QUEUE_PATH)

    if "source_id" not in queue_df.columns:
        queue_df["source_id"] = pd.NA

    for df in [master_df, queue_df]:
        for col in df.columns:
            df[col] = (df[col].astype("string").str.strip())

    master_df = master_df.replace(r"^\s*$", pd.NA, regex=True)

    queue_df = queue_df.replace(r"^\s*$", pd.NA, regex=True)

    logger.info(f"Master rows: {len(master_df)}")

    logger.info(f"Queue rows: {len(queue_df)}")

    master_index = set(
        master_df["source_id"].dropna().astype(str)
    )

    existing_ids = set(master_df["source_id"].dropna().astype(str))

    source_counters = {}

    new_rows = []

    for _, row in queue_df.iterrows():
        if pd.isna(row["source_id"]):
            base = (f"{slugify(row['regatta_name'])}_{row['year']}")

            counter = source_counters.get(base, 0) + 1

            source_id = generate_source_id(row["regatta_name"], row["year"], counter)

            while source_id in existing_ids:
                counter += 1

                source_id = generate_source_id(row["regatta_name"], row["year"], counter)

            source_counters[base] = counter

            queue_df.at[_, "source_id"] = source_id

            row["source_id"] = source_id

            existing_ids.add(source_id)

        key = row["source_id"]

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

def slugify(text):
    text = text.lower()

    text = re.sub(r"[^a-z0-9]+", "_", text)

    text = text.strip("_")

    return text

def generate_source_id(regatta_name, year, counter):
    base = (f"{slugify(regatta_name)}_{year}")

    return f"{base}_{counter}"
