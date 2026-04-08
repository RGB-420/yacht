import pandas as pd
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from app.core.base_scraper import BaseScraper


class SaileventScraper(BaseScraper):

    def __init__(self):
        super().__init__("sailevent")


    def scrape(self, url, browser):
        page = browser.new_page()

        self.logger.info(f"[STEP] Scraping URL: {url}")

        try:
            data = self.obtener_datos(page, url)

            df = pd.DataFrame(data)
            df = df.drop_duplicates()

            self.logger.info(f"[END] Total rows scraped: {len(df)}")

            return df

        except Exception as e:
            self.logger.error(f"[FAIL] Error in scrape(): {e}", exc_info=True)
            return None


    def get_column_map(self, table):
        header_row = table.locator("tbody tr").first
        header_cells = header_row.locator("th")

        col_map = {}

        for i in range(header_cells.count()):
            text = header_cells.nth(i).inner_text().strip().lower()

            if "class" in text:
                col_map["Class"] = i
            elif "sailno" in text or "no" in text:
                col_map["SailNo"] = i
            elif "club" in text:
                col_map["Club"] = i

        self.logger.info(f"[INFO] Column map: {col_map}")

        return col_map


    def accept_cookies(self, page, timeout=3000):
        try:
            page.locator("#ButtonEnter").wait_for(state="visible", timeout=timeout)
            page.locator("#ButtonEnter").click()
            self.logger.info("[INFO] Cookies accepted")
        except PlaywrightTimeoutError:
            self.logger.info("[INFO] No cookies popup found")


    def obtener_datos(self, page, url: str):
        self.logger.info("[STEP] Loading page")

        page.goto(url)
        page.wait_for_timeout(2000)

        self.accept_cookies(page)

        page.select_option("#DDLEvents", label="Race Week 2025")
        page.wait_for_load_state("networkidle")

        class_select = page.locator("select").nth(1)
        options = class_select.locator("option")

        self.logger.info(f"[INFO] Classes found: {options.count()}")

        all_rows = []

        for i in range(options.count()):
            try:
                class_value = options.nth(i).get_attribute("value")
                class_name = options.nth(i).inner_text().strip()

                if not class_name:
                    continue

                self.logger.info(f"[CLASS] {class_name}")

                class_select.select_option(class_value)
                page.wait_for_timeout(1500)

                table = page.locator("table").nth(1)
                rows = table.locator("tbody tr")

                row_count = rows.count()

                if row_count < 2:
                    self.logger.warning(f"[SKIP] No data for class {class_name}")
                    continue

                col_map = self.get_column_map(table)

                for r in range(1, row_count):
                    row = rows.nth(r)
                    cells = row.locator("td")

                    if cells.count() == 0:
                        continue

                    sailno = (
                        cells.nth(col_map["SailNo"]).inner_text().strip()
                        if "SailNo" in col_map else None
                    )

                    club = (
                        cells.nth(col_map["Club"]).inner_text().strip()
                        if "Club" in col_map else None
                    )

                    class_value_row = (
                        cells.nth(col_map["Class"]).inner_text().strip()
                        if "Class" in col_map else class_name
                    )

                    if not sailno:
                        continue
                    
                    all_rows.append({
                        "Boat Number": sailno,
                        "Club": club,
                        "Class": class_value_row
                    })

                self.logger.info(f"[OK] {row_count - 1} rows scraped for {class_name}")

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing class {class_name}: {e}", exc_info=True)

        self.logger.info(f"[INFO] Total boats extracted: {len(all_rows)}")

        return all_rows


def scrape(url, browser):
    scraper = SaileventScraper()
    return scraper.run(url, browser)