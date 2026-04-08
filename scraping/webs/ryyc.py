import pandas as pd
from bs4 import BeautifulSoup

from app.core.base_scraper import BaseScraper


COLUMN_MAP = {
    "sailno": "Sail No.",
    "boat": "Boat",
    "club": "Club",
    "type": "Design",
    "owner": "Person"
}


class RYYCScraper(BaseScraper):

    def __init__(self):
        super().__init__("ryyc")


    def scrape(self, url, browser):
        df = pd.DataFrame()
        page = browser.new_page()

        self.logger.info(f"[STEP] Scraping URL: {url}")

        try:
            html = self.get_html_with_playwright(page, url)

            if html:
                data = self.obtener_barcos(html)

                if data:
                    df_temp = pd.DataFrame(data)
                    df = pd.concat([df, df_temp], ignore_index=True)

                    self.logger.info(f"[OK] Scraped {len(df_temp)} rows")

                else:
                    self.logger.warning("[EMPTY] No boats found")

            else:
                self.logger.error("[FAIL] Could not retrieve HTML")
                return None

        except Exception as e:
            self.logger.error(f"[FAIL] Error in scrape(): {e}", exc_info=True)
            return None

        df = df.dropna(how='all')
        df = df.drop_duplicates(subset=['sailno', 'boat'], keep="first")

        return df


    def get_html_with_playwright(self, page, url: str) -> str:
        try:
            page.goto(url)
            page.wait_for_load_state("networkidle")
            return page.content()
        except Exception as e:
            self.logger.error(f"[FAIL] Error loading {url}: {e}", exc_info=True)
            return None


    def get_column_indices(self, tabla):
        header = tabla.find("thead").find_all("th")

        col_index = {}
        for i, th in enumerate(header):
            col_name = th.get_text(strip=True)
            col_index[col_name] = i

        self.logger.info(f"[INFO] Headers detected: {list(col_index.keys())}")

        return col_index


    def get_cell_text(self, cells, idx):
        if idx is None or idx >= len(cells):
            return None
        return cells[idx].get_text(strip=True)


    def obtener_barcos(self, html):
        soup = BeautifulSoup(html, "html.parser")
        tablas = soup.find_all("table", class_="pretty")

        self.logger.info(f"[INFO] Tables found: {len(tablas)}")

        datos = []

        for i, tabla in enumerate(tablas):
            try:
                self.logger.info(f"[STEP] Processing table {i}")

                indices = self.get_column_indices(tabla)
                cols = {k: indices.get(v) for k, v in COLUMN_MAP.items()}

                filas = tabla.find("tbody").find_all("tr")

                for fila in filas:
                    datos_barco = fila.find_all("td")

                    fila_datos = {
                        key: self.get_cell_text(datos_barco, idx)
                        for key, idx in cols.items()
                    }

                    datos.append(fila_datos)

                self.logger.info(f"[OK] Table {i} processed ({len(filas)} rows)")

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing table {i}: {e}", exc_info=True)

        self.logger.info(f"[INFO] Total boats scraped: {len(datos)}")

        return datos


# 🔥 Wrapper
def scrape(url, browser):
    scraper = RYYCScraper()
    return scraper.run(url, browser)