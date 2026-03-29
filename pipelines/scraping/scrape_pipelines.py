from scraping.runner import scrape_web, scrape_pdfs

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

def run_scrape_pipeline():
    logger.info("===== START SCRAPE PIPELINE =====")

    logger.info("Running web scrapers")
    scrape_web()

    logger.info("Running PDF scrapers")
    scrape_pdfs()

    logger.info("===== END SCRAPE PIPELINE =====")