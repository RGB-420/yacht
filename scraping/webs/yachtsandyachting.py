import pandas as pd

from app.core.base_scraper import BaseScraper


class YachtsAndYachtingScraper(BaseScraper):

    def __init__(self):
        super().__init__("yachtsandyachting")


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


    def normalizar_columnas(self, table):
        col = {}

        header_row = table.locator("tbody tr").first
        headers = header_row.locator("th")

        for i in range(headers.count()):
            name = headers.nth(i).inner_text().strip()
            name = name.replace("\xa0", "").lower()
            col[name] = i

        self.logger.info(f"[INFO] Column map: {col}")

        return col


    def get_value(self, cells, col_map, key):
        idx = col_map.get(key.lower())

        if idx is None or idx >= cells.count():
            return None

        return cells.nth(idx).inner_text().strip()


    def obtener_datos(self, page, url: str):
        self.logger.info("[STEP] Loading page")

        page.goto(url)
        page.wait_for_timeout(2000)

        boats = []

        table = page.locator("table.results")

        col_map = self.normalizar_columnas(table)

        rows = table.locator("tbody tr")

        row_count = rows.count()
        self.logger.info(f"[INFO] Rows found: {row_count}")

        for i in range(row_count):
            row = rows.nth(i)

            if row.locator("td").count() == 0:
                continue

            cells = row.locator("td")

            data = {
                "sail_number": self.get_value(cells, col_map, "sail no"),
                "boat_name": self.get_value(cells, col_map, "boat name"),
                "owner": self.get_value(cells, col_map, "owner(s)"),
                "club": self.get_value(cells, col_map, "club")
            }

            boats.append(data)

        self.logger.info(f"[INFO] Boats extracted: {len(boats)}")

        return boats


def scrape(url, browser):
    scraper = YachtsAndYachtingScraper()
    return scraper.run(url, browser)