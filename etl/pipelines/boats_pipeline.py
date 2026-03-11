from datetime import datetime
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
from db.repositories.raw_results_repo import get_all_raw_results

from domain.masters.master_boats import generate_master_boats

from utils.boats_transformation import explode_boats_for_db

def run_boats_pipeline():
    print("Running boats pipeline...")

    engine = get_engine()

    with engine.connect() as conn:
        df_raw = get_all_raw_results(conn)

    if df_raw.empty:
        print("No raw results")
        return
    
    df_master = generate_master_boats(df_raw)

    df_master = explode_boats_for_db(df_master)

    inserted_boats = 0
    inserted_owners = 0
    inserted_types = 0

    with engine.begin() as conn:
        for _, row in df_master.iterrows():
            source = row["Source"]

            if "-" not in source:
                raise ValueError(f"Invalid source format: {source}")
            
            regatta_name, year = source.rsplit("-", 1)
            year = int(year)

            edition_id = get_edition_id(conn, regatta_name, year)

            if not edition_id:
                raise ValueError(f"Edition not found: {regatta_name} {year}")

            # Get class
            class_name = row["Class"]
            class_id = get_class_id(conn, class_name)

            if not class_id:
                raise ValueError(f"Class not found: {class_name}")
            
            # Get club
            club_name = row["Club"]
            club_id = get_club_id(conn, club_name)

            if not club_id:
                raise ValueError(f"Club not found: {club_name}")
            
            # Insert type
            type_name = row["Boat Type"]
            if pd.notna(type_name) and str(type_name).strip() != "":
                type_id, created_type = upsert_boat_type(conn, type_name, class_id)

                if created_type:
                    inserted_types += 1

            # Insert owner
            owner_name = row["Owner"]
            owner_id, created_owner = upsert_owner(conn, owner_name)

            if created_owner:
                inserted_owners += 1

            # Insert boat
            boat_id_value = row["Boat Id"]
            boat_id, created_boat = upsert_boat(conn, row["Name"], boat_id_value, type_id)

            if created_boat:
                inserted_boats += 1

            # Relations
            insert_boat_owner(conn, boat_id, owner_id)
            insert_boat_club(conn, boat_id, club_id)
            insert_boat_edition(conn, boat_id, edition_id)
            insert_edition_class(conn, edition_id, class_id)

    print(f"Boats inserted: {inserted_boats}")
    print(f"Owners inserted: {inserted_owners}")
    print(f"Types inserted: {inserted_types}")
    print("Boats DB pipeline finished")           
