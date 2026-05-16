from scraping.runner import scrape_regattas

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

def run_scrape_pipeline():
    logger.info("===== START SCRAPE PIPELINE =====")

    scrape_regattas()

    logger.info("===== END SCRAPE PIPELINE =====")