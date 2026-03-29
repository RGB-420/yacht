from pathlib import Path
import pandas as pd

from db.connection import get_engine
from app.repositories.boat_classes_repo import upsert_boat_classes

from app.services.masters.master_classes import generate_master_classes
from app.core.config import DATA_MASTER

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

CLASSES_FILE = DATA_MASTER / "classes_master.csv"

def run_classes_pipeline():
    logger.info("===== START CLASSES PIPELINE =====")

    if not CLASSES_FILE.exists():
        logger.error("classes_master.csv not found")
        return
    
    logger.info(f"Reading file: {CLASSES_FILE}")

    df = generate_master_classes(CLASSES_FILE)

    df = df.astype(object).where(pd.notna(df), None)

    if df.empty:
        logger.warning("Generated classes dataframe is empty")

    logger.info(f"Rows loaded: {len(df)}")

    engine = get_engine()

    inserted_classes = 0

    logger.info("Starting database insertion")

    with engine.begin() as conn:
        for _, row in df.iterrows():
            class_id, created = upsert_boat_classes(conn,
                                                    name=row['name'],
                                                    manufacturer=row['manufacturer'],
                                                    category=row['category'],
                                                    rating_rule=row['rating_rule'],
                                                    start_year=row['start_year'],
                                                    crew_min=row['crew_min'],
                                                    crew_max=row['crew_max'],
                                                    length_m=row['length_m'])
            
            if created:
                inserted_classes += 1
    
    logger.info(f"Classes inserted: {inserted_classes}")
    logger.info("===== END CLASSES PIPELINE =====")
    