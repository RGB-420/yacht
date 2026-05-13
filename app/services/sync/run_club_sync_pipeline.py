from app.services.sync.sync_review_files import sync_unresolved_to_review, sync_pending_to_review

from app.services.sync.split_review_mapping import split_review_mapping

from app.services.sync.club_norm_sync import sync_club_norm

from app.services.sync.club_mapping_sync import sync_club_mapping

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

def run_club_sync_pipeline(conn):
    logger.info("===== START CLUB SYNC =====")

    sync_pending_to_review()

    sync_unresolved_to_review()

    split_review_mapping()

    sync_club_norm(conn)

    sync_club_mapping(conn)

    logger.info("===== END CLUB SYNC =====")
