import pandas as pd

from app.repositories.schedule_repo import get_all_schedule_with_regatta

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

def sync_schedule_csv_with_db(conn, csv_path):
    logger.info("Starting schedule CSV sync")

    if csv_path.exists():
        df = pd.read_csv(csv_path)
        logger.info(f"CSV loaded: {len(df)} rows")
    else:
        logger.warning("Schedule CSV not found, creating new one")
        df = pd.DataFrame(columns=["regatta_name", "year", "start_date", "end_date"])

    db_rows = get_all_schedule_with_regatta(conn)

    db_schedule = pd.DataFrame(
        db_rows,
        columns=["regatta_name", "year", "start_date", "end_date"]
    )

    logger.info(f"DB schedule rows: {len(db_schedule)}")
    
    if db_schedule.empty:
        logger.warning("No schedule data in DB")
        return

    csv_keys = set(zip(df["regatta_name"], df["year"]))
    db_keys = set(zip(db_schedule["regatta_name"], db_schedule["year"]))

    new_keys = db_keys - csv_keys

    new_rows = db_schedule[
        db_schedule.apply(lambda x: (x["regatta_name"], x["year"]) in new_keys, axis=1)
    ]

    if not new_rows.empty:
        logger.info(f"{len(new_rows)} new schedule entries found -> adding to CSV")

        df_updated = pd.concat([df, new_rows], ignore_index=True)
        df_updated.to_csv(csv_path, index=False)

        logger.info(f"{len(new_rows)} new schedule entries found → adding to CSV")

    else:
        logger.info(f"CSV updated: {csv_path}")

    logger.info("Finished schedule CSV sync")