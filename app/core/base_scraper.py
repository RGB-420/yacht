import time
import pandas as pd

from app.core.scraper_logger import get_scraper_logger


class BaseScraper:

    def __init__(self, name: str):
        self.logger = get_scraper_logger(name)

    def run(self, *args, **kwargs) -> pd.DataFrame | None:
        start_time = time.time()

        self.logger.info(f"[START] Scraper started | name={self.logger.name}")

        try:
            df = self.scrape(*args, **kwargs)

            duration = round(time.time() - start_time, 2)

            if df is None:
                self.logger.warning("[WARNING] Scraper returned None")
                rows = 0
            elif len(df) == 0:
                self.logger.warning("[EMPTY] Scraper returned empty DataFrame")
                rows = 0
            else:
                rows = len(df)

            self.logger.info(
                f"[END] Scraper finished | rows={rows} | time={duration}s | name={self.logger.name}"
            )

            return df

        except Exception as e:
            self.logger.error(f"[FAIL] Scraper crashed: {e}", exc_info=True)
            return None

    def scrape(self, *args, **kwargs) -> pd.DataFrame:
        raise NotImplementedError("Each scraper must implement scrape()")