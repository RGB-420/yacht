from pathlib import Path
import pandas as pd

from db.connection import get_engine
from db.repositories.clubs_repo import upsert_club
from db.repositories.locations_repo import get_or_create_location

from domain.masters.master_clubs import generate_master_clubs

from utils.clubs_sync import sync_clubs_csv_with_db

CLUBS_FILE = Path("data/master/clubs_master.csv")
RAW_CLUBS_FILE = Path("data/raw/clubs_master_raw.csv")

def run_clubs_pipeline():
    print("Running clubs pipeline...")

    if not CLUBS_FILE.exists():
        print("clubs_master.csv not found")
        return
    
    df = generate_master_clubs(CLUBS_FILE)

    engine = get_engine()

    inserted_clubs = 0
    inserted_locations = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            location_id, created_location = get_or_create_location(conn, city=row['city'], region=row['region'], country=row['country'])

            if created_location:
                inserted_locations += 1

            club_id, created_club = upsert_club(conn, name=row['name'], short_name=row['short_name'], estimated_numbers=row['estimated_numbers'], location_id=location_id)

            if created_club:
                inserted_clubs += 1

        sync_clubs_csv_with_db(conn, df, RAW_CLUBS_FILE)

    print(f"Locations inserted: {inserted_locations}")
    print(f"Clubs inserted: {inserted_clubs}")
    print("Clubs pipeline finished")