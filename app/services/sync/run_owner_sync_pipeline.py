from app.services.sync.owner_mapping_sync import sync_owner_mapping

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

def run_owner_sync_pipeline():
    logger.info("===== START OWNER SYNC =====")

    sync_owner_mapping()

    logger.info("===== END OWNER SYNC =====")