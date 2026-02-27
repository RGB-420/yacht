from pathlib import Path
import pandas as pd

from db.connection import get_engine
from db.repositories.boat_classes_repo import get_class_id
from db.repositories.clubs_repo import get_club_id
from db.repositories.owners_repo import upsert_owner
from db.repositories.boats_repo import upsert_boat
from db.repositories.boats_owner_repo import insert_boat_owner
from db.repositories.editions_repo import get_edition_id
from db.repositories.edition_classes_repo import insert_edition_class
from db.repositories.boat_type_repo import upsert_boat_type
from db.repositories.boat_clubs_repo import insert_boat_club
from db.repositories.boat_editions_repo import insert_boat_edition

from utils.boats_transformation import explode_boats_for_db

MASTER_FILE = Path("data/processed/master/Boats.csv")

def run_boats_db_pipeline():
    print("Running boats DB pipeline...")

    if not MASTER_FILE.exists():
        print("Boats master not found")
        return
    
    df = pd.read_csv(MASTER_FILE)

    df = explode_boats_for_db(df)
    
    engine = get_engine()

    inserted_boats = 0
    inserted_owners = 0
    inserted_types = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():

            # Get regatta name and year
            source = row["Source"]

            if "-" not in source:
                raise ValueError(f"Invalid source format: {source}")
            
            regatta_name, year = source.rsplit("-", 1)
            year = int(year)

            # Get edition
            edition_id = get_edition_id(conn, regatta_name, year)

            if not edition_id:
                raise ValueError(f"Edition not found for {regatta_name} {year}")
            
            # Get class
            class_name = row["Class"]
            class_id = get_class_id(conn, class_name)

            if not class_id:
                raise ValueError(f"Class not found: {class_name}")
            
            # Insert type
            type_name = row["Boat Type"]
            if pd.notna(type_name) and str(type_name).strip() != "":
                type_id, created_type = upsert_boat_type(conn, type_name, class_id)

                if created_type:
                    inserted_types += 1

            # Get club
            club_name = row["Club"]
            club_id = get_club_id(conn, club_name)

            if not club_id:
                raise ValueError(f"Club not found: {club_name}")

            # Insert owner
            owner_name = row["Owner"]
            owner_id, created_owner  = upsert_owner(conn, owner_name)

            if created_owner:
                inserted_owners += 1

            # Insert boat
            boat_id_value = row["Boat Id"]
            boat_id, created_boat = upsert_boat(conn, row["Name"], boat_id_value, class_id)

            if created_boat:
                inserted_boats += 1

            # Relations
            insert_boat_owner(conn, boat_id, owner_id)

            insert_edition_class(conn, edition_id, class_id)

            insert_boat_club(conn, boat_id, club_id)

            insert_boat_edition(conn, boat_id, edition_id)

    print(f"Boats inserted: {inserted_boats}")
    print(f"Owners inserted: {inserted_owners}")
    print(f"Types inserted: {inserted_types}")
    print("Boats DB pipeline finished")