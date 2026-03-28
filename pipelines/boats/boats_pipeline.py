from datetime import datetime
from pathlib import Path
import pandas as pd

from db.connection import get_engine
from app.repositories.boat_classes_repo import get_class_id
from app.repositories.clubs_repo import upsert_club
from app.repositories.owners_repo import upsert_owner
from app.repositories.boats_repo import upsert_boat
from app.repositories.boats_owner_repo import insert_boat_owner
from app.repositories.editions_repo import get_edition_id
from app.repositories.edition_classes_repo import insert_edition_class
from app.repositories.boat_type_repo import upsert_boat_type
from app.repositories.boat_clubs_repo import insert_boat_club
from app.repositories.boat_editions_repo import insert_boat_edition
from app.repositories.raw_results_repo import get_all_raw_results

from app.services.masters.master_boats import generate_master_boats

from app.services.normalizers.columns import normalize_columns

from app.services.aggregation.boats_transformation import explode_boats_for_db

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

def run_boats_pipeline():
    logger.info("===== START BOATS PIPELINE =====")

    engine = get_engine()

    with engine.connect() as conn:
        df_raw = get_all_raw_results(conn)
        logger.info(f"Raw rows: {len(df_raw)}")

    if df_raw.empty:
        logger.warning("No raw results found")
        return
    
    df_normalized = normalize_columns(df_raw)
    logger.info(f"Normalized rows: {len(df_normalized)}")

    df_master = generate_master_boats(df_normalized)

    df_master = explode_boats_for_db(df_master)

    inserted_boats = 0
    inserted_owners = 0
    inserted_types = 0
    inserted_clubs = 0

    with engine.begin() as conn:

        prenorm = {
            "class": set(),
            "club": set(),
            "boat_type": set(),
        }

        for _, row in df_master.iterrows():
            source = row["Source"]

            if "-" not in source:
                logger.error(f"Invalid source format: {source}")
                raise ValueError(f"Invalid source format: {source}")
            
            regatta_name, year = source.rsplit("-", 1)
            year = int(year)

            edition_id = get_edition_id(conn, regatta_name, year)
            if not edition_id:
                logger.error(f"Edition not found: {regatta_name} {year}")
                raise ValueError(f"Edition not found: {regatta_name} {year}")

            # Get class
            class_name = row["Class"]
            class_id = None
            if pd.notna(class_name) and str(class_name).strip() != "":
                class_id = get_class_id(conn, class_name)
                
                if not class_id:
                    prenorm["class"].add(class_name)
                    logger.warning(f"Classes not found: {prenorm['class']}")
            
            # Get club
            club_name = row["Club"]
            club_id = None

            if pd.notna(club_name) and str(club_name).strip() != "":
                club_id, created_club = upsert_club(conn, club_name)

                if created_club:
                    inserted_clubs += 1

            # Insert type
            type_name = row["Boat Type"]
            type_id = None

            if pd.notna(type_name) and str(type_name).strip() != "":
                type_id, created_type = upsert_boat_type(conn, type_name, class_id)

                if created_type:
                    inserted_types += 1

            # Insert owner
            owner_name = row["Owner"]

            if pd.isna(owner_name) or str(owner_name).strip() == "":
                owner_id = None
            else:
                owner_id, created_owner = upsert_owner(conn, owner_name)

                if created_owner:
                    inserted_owners += 1

            # Insert boat
            boat_id_value = row["Boat Id"]

            boat_id, created_boat = upsert_boat(conn, row["Name"], boat_id_value, type_id)

            if created_boat:
                inserted_boats += 1

            # Relations
            if owner_id:
                insert_boat_owner(conn, boat_id, owner_id)
            
            if club_id:
                insert_boat_club(conn, boat_id, club_id)
                
            insert_boat_edition(conn, boat_id, edition_id)
            
            if class_id:
                insert_edition_class(conn, edition_id, class_id)

    logger.info(f"Boats inserted: {inserted_boats}")
    logger.info(f"Owners inserted: {inserted_owners}")
    logger.info(f"Types inserted: {inserted_types}")
    logger.info(f"Clubs inserted: {inserted_clubs}")

    logger.info("===== END BOATS PIPELINE =====")  
