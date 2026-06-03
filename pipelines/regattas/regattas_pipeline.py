import pandas as pd

from db.connection import get_engine
from app.repositories.regattas_repo import upsert_regatta
from app.repositories.editions_repo import upsert_edition
from app.repositories.regatta_links_repo import upsert_regatta_link
from app.repositories.locations_repo import get_or_create_location
from app.repositories.schedule_repo import upsert_regatta_schedule

from app.services.masters.master_regattas import generate_master_regattas
from app.core.config import DATA_MASTER, DATA_RAW

from pipelines.regattas.regattas_sync import sync_regattas_csv_with_db

from pipelines.operations.sync_scrape_queue import sync_scrape_queue
from pipelines.operations.generate_unscraped_regattas import generate_unscraped_regattas

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

REGATTAS_FILE = DATA_MASTER / "regattas_master.csv"

RAW_REGATTAS_FILE = DATA_RAW / "regattas_master_raw.csv"

def run_regattas_pipeline():
    logger.info("===== START REGATTAS PIPELINE =====")

    sync_scrape_queue()

    if not REGATTAS_FILE.exists():
        logger.error("regattas_master.csv not found")
        return
    
    logger.info(f"Reading file: {REGATTAS_FILE}")
    
    df = generate_master_regattas(REGATTAS_FILE)
    logger.info(f"Rows loaded: {len(df)}")

    if df.empty:
        logger.warning("Generated regattas dataframe is empty")

    engine = get_engine()

    inserted_regattas = 0
    inserted_editions = 0
    inserted_links = 0
    updated_schedules = 0

    logger.info("Starting database insertion")

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

            if pd.notna(row.link):
                created_link = upsert_regatta_link(conn, edition_id, row.link)

                if created_link:
                    inserted_links += 1
            
            if pd.notna(row.start_date) and pd.notna(row.end_date):
                upsert_regatta_schedule(conn, edition_id, row.start_date.to_pydatetime(), row.end_date.to_pydatetime())

                updated_schedules += 1

        sync_regattas_csv_with_db(conn, df, RAW_REGATTAS_FILE)

    logger.info(f"Regattas inserted: {inserted_regattas}")
    logger.info(f"Editions inserted: {inserted_editions}")
    logger.info(f"Links inserted: {inserted_links}")
    logger.info(f"Schedules inserted: {updated_schedules}")

    generate_unscraped_regattas()

    logger.info("===== END REGATTAS PIPELINE =====")