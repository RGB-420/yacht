from app.services.sync.class_types.sync_review_files import sync_class_type_pending_to_review, sync_class_type_unresolved_to_review, sync_class_type_ignored_to_review
from app.services.sync.class_types.split_review_mapping import split_class_type_review
from app.services.sync.class_types.sync_class_types import sync_class_types
from app.services.sync.class_types.sync_class_type_mapping import sync_class_type_mapping

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

def run_class_type_sync_pipeline(conn):
    logger.info("===== START CLASS TYPE SYNC =====")

    sync_class_type_pending_to_review()

    sync_class_type_unresolved_to_review()

    sync_class_type_ignored_to_review()

    split_class_type_review()

    sync_class_types(conn)

    sync_class_type_mapping(conn)

    logger.info("===== END CLASS TYPE SYNC =====")