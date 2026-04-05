import pandas as pd

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

                    df = self.conseguir_owner_y_club(page, df)

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

        page.goto(url)
        page.wait_for_timeout(8000)

        boats = []

        table = page.locator("#main-table-container table")

        col_index = self.build_column_index(table)

        rows = table.locator("tbody tr")

        row_count = rows.count()
        self.logger.info(f"[INFO] Rows found: {row_count}")

        for i in range(row_count):
            row = rows.nth(i)
            cells = row.locator("td")

            fila_data = {
                "sailno": self.get_cell_text(cells, col_index, "sailno"),
                "boat": self.get_cell_text(cells, col_index, "boat"),
                "class": self.get_cell_text(cells, col_index, "class"),
                "club": self.get_cell_text(cells, col_index, "club"),
                "owner": self.get_cell_text(cells, col_index, "owner"),
                "boat_link": self.get_cell_link(cells, col_index, "boat"),
            }

            boats.append(fila_data)

        self.logger.info(f"[INFO] Boats extracted (base): {len(boats)}")

        return boats


    def conseguir_owner_y_club(self, page, df):
        BASE_URL = "https://yachtscoring.com"

        if "boat_url" not in df.columns:
            df["boat_url"] = BASE_URL + df["boat_link"]
            df = df.dropna(subset=["boat_url"])

        self.logger.info(f"[STEP] Enriching boats with detail pages ({len(df)})")

        for idx, row in df.iterrows():
            try:
                boat_url = row["boat_url"]

                self.logger.info(f"[DETAIL] {boat_url}")

                page.goto(boat_url)
                page.wait_for_timeout(2000)

                owner = None
                owner_locator = page.locator("div.font-bold", has_text="Name:")
                if owner_locator.count():
                    owner = (
                        owner_locator.first
                        .locator("..")
                        .locator("div")
                        .nth(1)
                        .inner_text()
                        .strip()
                    )

                club = None
                club_locator = page.locator("div.font-bold", has_text="Yacht Club:")
                if club_locator.count():
                    club = (
                        club_locator.first
                        .locator("..")
                        .locator("div")
                        .nth(1)
                        .inner_text()
                        .strip()
                    )

                df.loc[idx, "owner"] = owner
                df.loc[idx, "club"] = club

            except Exception as e:
                self.logger.error(f"[FAIL] Error enriching {row.get('boat_link')}: {e}", exc_info=True)

        return df


def scrape(url, browser):
    scraper = YachtScoringScraper()
    return scraper.run(url, browser)