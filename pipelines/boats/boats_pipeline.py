from datetime import datetime
from pathlib import Path
import pandas as pd

from db.connection import get_engine
from app.repositories.boat_classes_repo import load_class_cache
from app.repositories.clubs_repo import upsert_club, load_club_cache
from app.repositories.owners_repo import upsert_owner, load_owner_cache
from app.repositories.boats_repo import upsert_boat, load_boat_cache
from app.repositories.boats_owner_repo import insert_boat_owner
from app.repositories.editions_repo import load_edition_cache
from app.repositories.edition_classes_repo import insert_edition_class
from app.repositories.boat_type_repo import upsert_boat_type, load_type_cache
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

    df_master = generate_master_boats(df_normalized)

    logger.info(f"Master boat rows: {len(df_master)}")

    df_master = explode_boats_for_db(df_master)

    logger.info(f"Exploded rows: {len(df_master)}")

    inserted_boats = 0
    inserted_owners = 0
    inserted_types = 0
    inserted_clubs = 0

    with engine.begin() as conn:
        edition_cache = load_edition_cache(conn)
        class_cache = load_class_cache(conn)
        club_cache = load_club_cache(conn)
        type_cache = load_type_cache(conn)
        owner_cache = load_owner_cache(conn)
        boat_cache = load_boat_cache(conn)

        logger.info(f"Edition cache: {len(edition_cache)}")
        logger.info(f"Class cache: {len(class_cache)}")
        logger.info(f"Club cache: {len(club_cache)}")
        logger.info(f"Type cache: {len(type_cache)}")
        logger.info(f"Owner cache: {len(owner_cache)}")
        logger.info(f"Boat cache: {len(boat_cache)}")

        boat_owner_rel_cache = set()
        boat_club_rel_cache = set()
        boat_edition_rel_cache = set()
        edition_class_rel_cache = set()

        prenorm = {
            "class": set(),
            "club": set(),
            "boat_type": set(),
        }

        df_master.columns = [col.replace(" ", "_") for col in df_master.columns]

        for i, row in enumerate(df_master.itertuples(index=False)):

            if i % 100 == 0:
                logger.info(f"Processing row {i}/{len(df_master)}")
            source = row.Source

            if "-" not in source:
                logger.error(f"Invalid source format: {source}")
                raise ValueError(f"Invalid source format: {source}")
            
            regatta_name, year = source.rsplit("-", 1)
            year = int(year)

            edition_key = (regatta_name, year)

            edition_id = edition_cache.get(edition_key)

            if not edition_id:
                logger.error(f"Edition not found: {regatta_name} {year}")
                raise ValueError(f"Edition not found: {regatta_name} {year}")

            # Get class
            class_name = row.Class
            class_id = None

            if pd.notna(class_name) and str(class_name).strip() != "":
                class_id = class_cache.get(class_name)
                
                if not class_id:
                    prenorm["class"].add(class_name)
            
            # Get club
            club_name = row.Club
            club_id = None

            if pd.notna(club_name) and str(club_name).strip() != "":
                if club_name in club_cache:
                    club_id = club_cache[club_name]

                else:
                    club_id, created_club = upsert_club(conn, club_name)

                    club_cache[club_name] = club_id

                    if created_club:
                        inserted_clubs += 1

            # Insert type
            type_name = row.Boat_Type
            type_id = None

            if pd.notna(type_name) and str(type_name).strip() != "":
                type_key = (type_name, class_id)

                if type_key in type_cache:
                    type_id = type_cache[type_key]

                else:
                    type_id, created_type = upsert_boat_type(conn, type_name, class_id)
                    type_cache[type_key] = type_id

                    if created_type:
                        inserted_types += 1

            # Insert owner
            owner_name = row.Owner

            if pd.isna(owner_name) or str(owner_name).strip() == "":
                owner_id = None
            else:
                if owner_name in owner_cache:
                    owner_id = owner_cache[owner_name]

                else:
                    owner_id, created_owner = upsert_owner(conn, owner_name)

                    owner_cache[owner_name] = owner_id

                    if created_owner:
                        inserted_owners += 1

            # Insert boat
            boat_id_value = row.Boat_Id

            boat_key = (row.Name, boat_id_value)

            if boat_key in boat_cache:
                boat_id = boat_cache[boat_key]
                created_boat = False
            else:
                boat_id, created_boat = upsert_boat(conn, row.Name, boat_id_value, type_id)

                boat_cache[boat_key] = boat_id

                if created_boat:
                    inserted_boats += 1

            # Relations
            if owner_id:
                relation_key = (boat_id, owner_id)

                if relation_key not in boat_owner_rel_cache:
                    insert_boat_owner(conn, boat_id, owner_id)
                    boat_owner_rel_cache.add(relation_key)

            if club_id:
                relation_key = (boat_id, club_id)

                if relation_key not in boat_club_rel_cache:
                    insert_boat_club(conn, boat_id, club_id)
                    boat_club_rel_cache.add(relation_key)
                
            relation_key = (boat_id, edition_id)

            if relation_key not in boat_edition_rel_cache:    
                insert_boat_edition(conn, boat_id, edition_id)
                boat_edition_rel_cache.add(relation_key)
            
            if class_id:
                relation_key = (edition_id, class_id)

                if relation_key not in edition_class_rel_cache:
                    insert_edition_class(conn, edition_id, class_id)
                    edition_class_rel_cache.add(relation_key)

    if prenorm["class"]:
        logger.warning(f"Classes not found: {prenorm['class']}")

    logger.info(f"Boats inserted: {inserted_boats}")
    logger.info(f"Owners inserted: {inserted_owners}")
    logger.info(f"Types inserted: {inserted_types}")
    logger.info(f"Clubs inserted: {inserted_clubs}")

    logger.info("===== END BOATS PIPELINE =====")  
