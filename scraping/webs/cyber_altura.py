import pandas as pd
import requests
from bs4 import BeautifulSoup

from app.core.base_scraper import BaseScraper


COLUMN_MAP = { 
    "sailno": ["Nº.Vela", "N.Vela", "Sail nr."],
    "boat": ["Yate", "Boat Name", "Yacht"],
    "type": ["Boat type", "Design Class", "Modelo", "Type"],
    "club": ["Club"],
    "owner": ["Armador", "Patrón", "Patron"],
}


class CyberAlturaScraper(BaseScraper):

    def __init__(self):
        super().__init__("cyberaltura")


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

        df = df.dropna(axis=1, how="all")

        return df


    def get_html_with_playwright(self, page, url: str) -> str:
        try:
            page.goto(url)
            page.wait_for_load_state("networkidle")
            return page.content()
        except Exception as e:
            self.logger.error(f"[FAIL] Error loading {url}: {e}", exc_info=True)
            return None


    def obtener_html(self, session, URL):
        try:
            response = session.get(URL, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"[FAIL] Error fetching {URL}: {e}")
            return None


    def resolve_columns(self, indices, column_map):
        normalized_indices = {
            k.lower().strip(): v
            for k, v in indices.items()
        }

        resolved = {}

        for logical_name, possible_headers in column_map.items():
            resolved[logical_name] = None

            for header in possible_headers:
                key = header.lower().strip()

                if key in normalized_indices:
                    resolved[logical_name] = normalized_indices[key]
                    break

        self.logger.info(f"[INFO] Resolved columns: {resolved}")

        return resolved


    def get_column_indices(self, tabla, header_keyword = None):
        rows = tabla.find_all("tr")

        header_row = None
        header_idx = 0

        for idx, tr in enumerate(rows):
            cells = tr.find_all(["th", "td"])

            texts = [c.get_text(strip=True) for c in cells]

            if header_keyword:
                if any(header_keyword.lower() in t.lower() for t in texts):
                    header_row = tr
                    header_idx = idx
                    break
        
        if header_row is None:
            self.logger.warning(f"[WARNING] Header keyword '{header_keyword}' not found. Using second row")

            if len(rows) > 1:
                header_row = rows[1]
            else:
                header_row = rows[0]

        headers = header_row.find_all(["th", "td"])

        col_index = {}

        for i, cell in enumerate(headers):
            col_name = cell.get_text(strip=True)
            col_index[col_name] = i

        self.logger.info(f"[INFO] Headers detected: {list(col_index.keys())}")

        return col_index, header_idx


    def get_cell_text(self, cells, idx):
        if idx is None or idx >= len(cells):
            return None
        return cells[idx].get_text(strip=True)


    def obtener_barcos(self, html):
        soup = BeautifulSoup(html, "html.parser")

        tablas = soup.find_all("table", class_=["fondoBlanco"])

        self.logger.info(f"[INFO] Tables found: {len(tablas)}")

        datos = []

        for table_idx, tabla in enumerate(tablas):
            try:
                self.logger.info(f"[STEP] Processing table {table_idx}")

                indices, header_idx = self.get_column_indices(tabla, header_keyword="Pos")
                cols = self.resolve_columns(indices, COLUMN_MAP)

                filas = tabla.find_all("tr")[header_idx + 1:]

                for fila in filas:
                    datos_barco = fila.find_all("td")

                    if not datos_barco:
                        continue

                    fila_datos = {
                        key: self.get_cell_text(datos_barco, idx)
                        for key, idx in cols.items()
                    }

                    if not any(v not in [None, ""] for v in fila_datos.values()):
                        continue

                    datos.append(fila_datos)

                self.logger.info(f"[OK] Table {table_idx} processed ({len(filas)} rows)")

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing table {table_idx}: {e}", exc_info=True)

        self.logger.info(f"[INFO] Total boats scraped: {len(datos)}")

        return datos


def scrape(url, browser):
    scraper = CyberAlturaScraper()
    return scraper.run(url, browser)
