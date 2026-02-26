from pathlib import Path

from db.connection import get_engine
from db.repositories.regattas_repo import upsert_regatta
from db.repositories.editions_repo import upsert_edition
from db.repositories.regatta_links_repo import upsert_regatta_link
from db.repositories.locations_repo import get_or_create_location

from domain.masters.master_regattas import generate_master_regattas


REGATTAS_FILE = Path("data/regattas_master.csv")


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
            location_id, _ = get_or_create_location(conn, city=row['city'], region=row['region'], country=row['country'])

            if not location_id:
                raise ValueError(f"Location not found: {row['city']}")

            regatta_id, created_regatta = upsert_regatta(conn, name=row.regatta_name, type=row.type, club_id=None, location_id=location_id)

            if created_regatta:
                inserted_regattas += 1

            edition_id, created_edition = upsert_edition(conn, regatta_id, row.year)

            if created_edition:
                inserted_editions += 1

            if row.link:
                created_link = upsert_regatta_link(conn, edition_id, row.link)

                if created_link:
                    inserted_links += 1

    print(f"Regattas inserted: {inserted_regattas}")
    print(f"Editions inserted: {inserted_editions}")
    print(f"Links inserted: {inserted_links}")
    print("Regattas pipeline finished.")