import pandas as pd

from app.core.base_scraper import BaseScraper


all_regatas = True
selected_regatas = []


class Events2Scraper(BaseScraper):

    def __init__(self):
        super().__init__("events2")


    def scrape(self, url, browser):
        page = browser.new_page()

        self.logger.info(f"[STEP] Scraping URL: {url}")

        try:
            page.goto(url)
            page.wait_for_load_state("domcontentloaded")

            data = self.obtener_datos(page, url)

        except Exception as e:
            self.logger.error(f"[FAIL] Error in scrape(): {e}", exc_info=True)
            return None

        finally:
            page.close()

        df = pd.DataFrame(data)
        df = df.drop_duplicates()

        return df


    def obtener_datos(self, page, url: str):
        self.logger.info("[STEP] Extracting data from page")

        page.goto(url)
        page.wait_for_load_state("domcontentloaded")

        boats = []

        tables = page.locator("table")
        num_tables = tables.count()

        self.logger.info(f"[INFO] Tables found: {num_tables}")

        for table_idx in range(num_tables):
            try:
                table = tables.nth(table_idx)
                rows = table.locator("tbody tr")

                row_count = rows.count()
                self.logger.info(f"[INFO] Table {table_idx}: {row_count} rows")

                for row_idx in range(1, row_count):  # skip header
                    row = rows.nth(row_idx)
                    cells = row.locator("td")

                    sail_number = cells.nth(0).inner_text().strip()
                    boat_name = cells.nth(1).inner_text().strip()

                    if not sail_number:
                        self.logger.warning(f"[SKIP] Empty sail number at table {table_idx}, row {row_idx}")
                        break

                    boats.append({
                        "sail_number": sail_number,
                        "boat_name": boat_name,
                    })

                self.logger.info(f"[OK] Table {table_idx} processed")

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing table {table_idx}: {e}", exc_info=True)

        self.logger.info(f"[INFO] Total boats scraped: {len(boats)}")

        return boats


def scrape(url, browser):
    scraper = Events2Scraper()
    return scraper.run(url, browser)