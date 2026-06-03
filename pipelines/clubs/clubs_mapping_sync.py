import pandas as pd

from app.repositories.club_aliases_repo import get_all_club_mappings

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

def sync_club_mapping_csv_with_db(conn, csv_path):
    logger.info("Starting club mapping sync")

    rows = get_all_club_mappings(conn)

    df = pd.DataFrame(rows)

    if df.empty:
        logger.warning("No club mappings found")
        return
    
    df.to_csv(csv_path, index=False)

    logger.info(f"Exported {len(df)} mappings")
    logger.info(f"CSV updated: {csv_path}")