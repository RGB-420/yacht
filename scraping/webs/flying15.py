import pandas as pd

from app.core.base_scraper import BaseScraper


col_name = 4
col_number = 3
col_club = 7
col_mna = 2


class Flying15Scraper(BaseScraper):

    def __init__(self):
        super().__init__("flying15")


    def scrape(self, url, browser):
        df = pd.DataFrame()

        page = browser.new_page()

        self.logger.info(f"[STEP] Scraping URL: {url}")

        if url:
            try:
                data = self.obtener_datos(page, url)

                if data:
                    df_temp = pd.DataFrame(data)
                    df = pd.concat([df, df_temp], ignore_index=True)

                    self.logger.info(f"[OK] Scraped {len(df_temp)} rows")

                else:
                    self.logger.warning("[EMPTY] No boats found")

            except Exception as e:
                self.logger.error(f"[FAIL] Error in scrape(): {e}", exc_info=True)
                return None
        else:
            self.logger.error("[FAIL] Invalid URL")
            return None

        df = df.drop_duplicates()

        return df


    def obtener_datos(self, page, url: str):
        self.logger.info("[STEP] Extracting table data")

        page.goto(url)
        page.wait_for_timeout(2000)

        boats = []

        table = page.locator("div.edNews_articleContent")
        rows = table.locator("table tbody tr")

        row_count = rows.count()
        self.logger.info(f"[INFO] Rows found: {row_count}")

        for i in range(row_count):
            try:
                row = rows.nth(i)
                cells = row.locator("td")

                if cells.count() < 4:
                    continue

                boat_name = cells.nth(col_name).inner_text().strip()
                sail_number = cells.nth(col_number).inner_text().strip()
                mna = cells.nth(col_mna).inner_text().strip()
                club = cells.nth(col_club).inner_text().strip()

                boats.append({
                    "boat_name": boat_name,
                    "sail_number": sail_number,
                    "club": club,
                    "mna": mna
                })

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing row {i}: {e}", exc_info=True)

        self.logger.info(f"[INFO] Total boats scraped: {len(boats)}")

        return boats


def scrape(url, browser):
    scraper = Flying15Scraper()
    return scraper.run(url, browser)