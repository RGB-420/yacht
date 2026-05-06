from pathlib import Path
import pandas as pd

from db.connection import get_engine
from app.repositories.editions_repo import get_edition_id
from app.repositories.schedule_repo import upsert_regatta_schedule_dates, get_schedule_with_dates

from app.services.masters.master_schedule import generate_master_schedule

from app.core.calendar_utils import generate_ics
from app.core.config import DATA_MASTER

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

SCHEDULE_FILE = DATA_MASTER / "schedule_master.csv"

def run_scheduled_pipeline():
    logger.info("===== START SCHEDULE PIPELINE =====")

    # Check file
    if not SCHEDULE_FILE.exists():
        logger.error("schedule_master.csv not found")
        return
    
    logger.info(f"Reading file: {SCHEDULE_FILE}")

    # Generate data
    df = generate_master_schedule(SCHEDULE_FILE)
    logger.info(f"Rows loaded: {len(df)}")

    if df.empty:
        logger.warning("Generated schedule dataframe is empty")

    engine = get_engine()

    updated = 0
    skipped_no_dates = 0
    skipped_not_found = 0

    logger.info("Starting schedule update in DB")

    with engine.begin() as conn:
        for _,row in df.iterrows():
            if pd.isna(row.start_date) or pd.isna(row.end_date):
                skipped_no_dates += 1
                continue

            edition_id = get_edition_id(conn, row.regatta_name, row.year)

            if not edition_id:
                logger.warning(f"Edition not found: {row.regatta_name} ({row.year})")
                skipped_not_found += 1
                continue

            schedule_id = upsert_regatta_schedule_dates(conn, edition_id, row.start_date, row.end_date)
            updated += 1

    logger.info(f"Schedules updated: {updated}")
    logger.info(f"Skipped (no dates): {skipped_no_dates}")
    logger.info(f"Skipped (not found): {skipped_not_found}")

    # Generate calendar
    logger.info("Generating calendar (.ics)")

    with engine.begin() as conn:
        events = get_schedule_with_dates(conn)

    logger.info(f"Events fetched for calendar: {len(events)}")

    # NOT REQUIRED IS IN THE WEB PAGE
    # generate_ics(events)

    # logger.info("Calendar .ics generated")

    logger.info("===== END SCHEDULE PIPELINE =====")