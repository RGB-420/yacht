import pandas as pd
import time

from app.core.base_scraper import BaseScraper


COLUMN_MAP = {
    "sailno": ["sailno", "sail number"],
    "boat": ["boat", "boat name", "yacht name"],
    "class": ["class"],
    "type": ["boat type", "yacht type"],
    "club": ["club", "yacht club"],
    "owner": ["owner", "owner's name"]
}


class YachtScoringScraper(BaseScraper):

    def __init__(self):
        super().__init__("yachtscoring")
        self.boat_cache = {}


    def scrape(self, url, browser):
        df = pd.DataFrame()
        page = browser.new_page()

        self.logger.info(f"[STEP] Scraping URL: {url}")

        try:
            if url:
                data = self.obtener_datos(page, url)

                if data:
                    df_temp = pd.DataFrame(data)
                    df = pd.concat([df, df_temp], ignore_index=True)

                    self.logger.info(f"[OK] Base table scraped ({len(df_temp)} rows)")

                    df = df.drop_duplicates()

                    df = self.conseguir_detalles(page, df)

                else:
                    self.logger.warning("[EMPTY] No boats found")

        except Exception as e:
            self.logger.error(f"[FAIL] Error in scrape(): {e}", exc_info=True)
            return None

        df = df.drop(columns=["boat_link", "boat_url"], errors="ignore")
        df = df.dropna(axis=1, how="all")

        self.logger.info(f"[END] Final dataset rows: {len(df)}")

        return df


    def normalize(self, text: str) -> str:
        return text.replace("\xa0", " ").strip().lower()


    def get_cell_text(self, cells, col_index, key):
        idx = col_index.get(key)
        if idx is None or idx >= cells.count():
            return None
        return cells.nth(idx).inner_text().strip()


    def get_cell_link(self, cells, col_index, key):
        idx = col_index.get(key)
        if idx is None or idx >= cells.count():
            return None

        link = cells.nth(idx).locator("a")
        if link.count() == 0:
            return None

        return link.first.get_attribute("href")


    def build_column_index(self, table):
        col_index = {}

        headers = table.locator("thead").first.locator("td")

        header_texts = [
            self.normalize(headers.nth(i).inner_text())
            for i in range(headers.count())
        ]

        for standard_name, variants in COLUMN_MAP.items():
            for i, header in enumerate(header_texts):
                if header in variants:
                    col_index[standard_name] = i
                    break

        self.logger.info(f"[INFO] Column index: {col_index}")

        return col_index


    def obtener_datos(self, page, url: str):
        self.logger.info("[STEP] Loading main table")
        selector = "table.ys-table tbody tr"

        page.goto(url)
        page.wait_for_selector(selector, timeout=10000)

        rows_loaded = self.wait_for_table_load(page, selector, 10, 1.0)

        boats = []

        table = page.locator("table.ys-table")

        col_index = self.build_column_index(table)

        tbodies = table.locator("tbody")
        tbody_count = tbodies.count()

        self.logger.info(f"[INFO] Tbodies found: {tbody_count}")

        for t in range(tbody_count):
            tbody = tbodies.nth(t)
            rows = tbody.locator("tr")

            row_count = rows.count()
            self.logger.info(f"[INFO] Rows in tbody {t}: {row_count}")

            for i in range(row_count):
                row = rows.nth(i)
                cells = row.locator("td")

                try:
                    fila_data = {
                        "sailno": self.get_cell_text(cells, col_index, "sailno"),
                        "boat": self.get_cell_text(cells, col_index, "boat"),
                        "class": self.get_cell_text(cells, col_index, "class"),
                        "club": self.get_cell_text(cells, col_index, "club"),
                        "owner": self.get_cell_text(cells, col_index, "owner"),
                        "boat_link": self.get_cell_link(cells, col_index, "boat"),
                        "type": self.get_cell_text(cells, col_index, "type")
                    }

                    boats.append(fila_data)

                except Exception as e:
                    self.logger.warning(f"[ROW SKIP] Error parsong row: {e}")

        self.logger.info(f"[INFO] Boats extracted (base): {len(boats)}")

        return boats


    def conseguir_detalles(self, page, df):
        BASE_URL = "https://yachtscoring.com"

        if "boat_url" not in df.columns:
            df["boat_url"] = BASE_URL + df["boat_link"]
            df = df.dropna(subset=["boat_url"])

        self.logger.info(f"[STEP] Enriching boats with detail pages ({len(df)})")

        for idx, row in df.iterrows():
            try:
                key = (row["boat"], row["sailno"])

                if key in self.boat_cache:
                    cached = self.boat_cache[key]

                    self.logger.info(f"[CACHE] Using cached data for {key}")

                    if cached.get("owner"):
                        df.loc[idx, "owner"] = cached["owner"]

                    if cached.get("club"):
                        df.loc[idx, "club"] = cached["club"]

                    if cached.get("type"):
                        df.loc[idx, "type"] = cached["type"]

                    continue

                boat_url = row["boat_url"]

                self.logger.info(f"[DETAIL] {boat_url}")

                page.goto(boat_url, wait_until="domcontentloaded")
                page.wait_for_selector("div:has-text('Name:')")

                self.wait_for_name_loaded(page)

                owner = None
                club = None
                boat_type = None

                owner = self.get_detail_value(page, "Name:")
                club = self.get_detail_value(page, "Yacht Club:")
                boat_type = self.get_detail_value(page, "Design:")

                if owner:
                    df.loc[idx, "owner"] = owner
                
                if club:
                    df.loc[idx, "club"] = club

                if boat_type:
                    df.loc[idx, "type"] = boat_type

                if owner or club or boat_type:
                    self.boat_cache[key] = {
                        "owner": owner,
                        "club": club,
                        "type": boat_type
                    }

            except Exception as e:
                self.logger.error(f"[FAIL] Error enriching {row.get('boat_link')}: {e}", exc_info=True)

        return df


    def wait_for_name_loaded(self, page, retries=5, delay=0.3):
        for _ in range(retries):
            name = self.get_detail_value(page, "Name:")
            if name and name.strip() != "":
                return True
            time.sleep(delay)
        return False

    def get_detail_value(self, page, label):
        locator = page.locator("div.flex.flex-row").filter(has_text=label)

        if locator.count() == 0:
            return None

        try:
            return (
                locator.first
                .locator("div")
                .nth(1)
                .inner_text()
                .strip()
            )
        except:
            return None
        
    
    def wait_for_table_load(self, page, selector, max_checks, delay):
        prev_count = 0

        for i in range(max_checks):
            current_count = page.locator(selector).count()

            if current_count == prev_count:
                break

            prev_count = current_count
            time.sleep(delay)

        return current_count

def scrape(url, browser):
    scraper = YachtScoringScraper()
    return scraper.run(url, browser)