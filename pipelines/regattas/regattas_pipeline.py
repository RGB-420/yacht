from pathlib import Path

from db.connection import get_engine
from app.repositories.regattas_repo import upsert_regatta
from app.repositories.editions_repo import upsert_edition
from app.repositories.regatta_links_repo import upsert_regatta_link
from app.repositories.locations_repo import get_or_create_location
from app.repositories.schedule_repo import upsert_regatta_schedule

from app.services.masters.master_regattas import generate_master_regattas

from pipelines.schedule.schedule_sync import sync_schedule_csv_with_db


REGATTAS_FILE = Path("data/master/regattas_master.csv")
SCHEDULE_FILE = Path("data/master/schedule_master.csv")


def run_regattas_pipeline():
    print("Running regattas pipeline...")

    if not REGATTAS_FILE.exists():
        print("regattas_master.csv not found.")
        return
    
    df = generate_master_regattas(REGATTAS_FILE)

    engine = get_engine()

    inserted_regattas = 0
    inserted_editions = 0
    inserted_links = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            location_id = None
            
            if any([row.city, row.region, row.country]):
                location_id, _ = get_or_create_location(conn, city=row["city"], region=row["region"], country=row["country"])

            regatta_id, created_regatta = upsert_regatta(conn, name=row.regatta_name, type=row.type, club_id=None, location_id=location_id)

            if created_regatta:
                inserted_regattas += 1

            edition_id, created_edition = upsert_edition(conn, regatta_id, row.year, row.status)

            if created_edition:
                inserted_editions += 1

            if row.link:
                created_link = upsert_regatta_link(conn, edition_id, row.link)

                if created_link:
                    inserted_links += 1
            
            if row.status == "future":
                scheduled_id = upsert_regatta_schedule(conn, edition_id)

        sync_schedule_csv_with_db(conn, SCHEDULE_FILE)

    print(f"Regattas inserted: {inserted_regattas}")
    print(f"Editions inserted: {inserted_editions}")
    print(f"Links inserted: {inserted_links}")
    print("Regattas pipeline finished.")