from scraping.runner import scrape_regattas

from pipelines.operations.sync_scrape_queue import sync_scrape_queue
from pipelines.operations.sync_unscraped_to_master import sync_unscraped_to_master
from pipelines.operations.generate_unscraped_regattas import generate_unscraped_regattas

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

def run_scrape_pipeline():
    logger.info("===== START SCRAPE PIPELINE =====")

    sync_scrape_queue()

    sync_unscraped_to_master()

    scrape_regattas()

    generate_unscraped_regattas()

    logger.info("===== END SCRAPE PIPELINE =====")