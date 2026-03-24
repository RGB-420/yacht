from pathlib import Path
import pandas as pd

from db.connection import get_engine
from db.repositories.editions_repo import get_edition_id
from db.repositories.schedule_repo import upsert_regatta_schedule_dates

from domain.masters.master_schedule import generate_master_schedule

SCHEDULE_FILE = Path("data/master/schedule_master.csv")

def run_scheduled_pipeline():
    print("Running schedule pipeline...")

    if not SCHEDULE_FILE.exists():
        print("schedule_master.csv not found")
        return
    
    df = generate_master_schedule(SCHEDULE_FILE)

    engine = get_engine()

    updated = 0
    skipped_no_dates = 0
    skipped_not_found = 0

    with engine.begin() as conn:
        for _,row in df.iterrows():
            if pd.isna(row.start_date) or pd.isna(row.end_date):
                skipped_no_dates += 1
                continue

            edition_id = get_edition_id(conn, row.regatta_name, row.year)

            if not edition_id:
                print(f"[WARNING] Edition not found: {row.regatta_name} ({row.year})")
                skipped_not_found += 1
                continue

            schedule_id = upsert_regatta_schedule_dates(conn, edition_id, row.start_date, row.end_date)
            updated += 1

    print(f"Schedules updated: {updated}")
    print(f"Skipped (no dates): {skipped_no_dates}")
    print(f"Skipped (not found): {skipped_not_found}")
    print("Scheduled pipeline finsihed")