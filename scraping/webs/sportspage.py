import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

from app.core.base_scraper import BaseScraper


COLUMN_MAP = { 
    "division": ["Fleet"],
    "sailno": ["Boat No", "Sail Number", "Sail number", "Sail_No"],
    "boat": ["Boat", "Boat Name"],
    "type": ["Class", "Boat type"],
    "club": ["Club", "Yacht Club"],
    "owner/club": ["Skipper/Crew", "Helm/Owner"],
    "mna": ["Boat MNA"],
}


class SportspageScraper(BaseScraper):

    def __init__(self):
        super().__init__("sportspage")


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

        df = df.replace("", pd.NA)         
        df = df.dropna(how="all") 
        
        return df


    def get_html_with_playwright(self, page, url: str) -> str:
        try:
            page.goto(url)
            page.wait_for_load_state("networkidle")
            return page.content()
        except Exception as e:
            self.logger.error(f"[FAIL] Error loading {url}: {e}", exc_info=True)
            return None


    def resolve_columns(self, indices, column_map):
        resolved = {}

        for logical_name, possible_headers in column_map.items():
            resolved[logical_name] = None
            for header in possible_headers:
                if header in indices:
                    resolved[logical_name] = indices[header]
                    break

        self.logger.info(f"[INFO] Resolved columns: {resolved}")

        return resolved


    def get_column_indices(self, tabla):
        header = tabla.find_all("tr")[0].find_all("td")

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


    def split_owner_club(self, text):
        if not text:
            return None, None
        
        match = re.match(r"(.+?)\((.+)\)", text)
        if match:
            return match.group(1).strip(), match.group(2).strip()
        
        return text, None

    def obtener_barcos(self, html):
        soup = BeautifulSoup(html, "html.parser")

        tablas = soup.find_all("table")

        self.logger.info(f"[INFO] Tables found: {len(tablas)}")

        datos = []

        for table_idx, tabla in enumerate(tablas):
            try:
                self.logger.info(f"[STEP] Processing table {table_idx}")

                indices = self.get_column_indices(tabla)
                cols = self.resolve_columns(indices, COLUMN_MAP)

                rows = tabla.find_all("tr")
                if len(rows) < 2:
                    return []

                header = rows[0].find_all("td")
                filas = rows[1:]

                for fila in filas:
                    datos_barco = fila.find_all("td")

                    owner_text = self.get_cell_text(datos_barco, cols.get("owner/club"))
                    owner, club = self.split_owner_club(owner_text)

                    fila_datos = {
                        "division": self.get_cell_text(datos_barco, cols.get("division")),
                        "sailno": self.get_cell_text(datos_barco, cols.get("sailno")),
                        "boat": self.get_cell_text(datos_barco, cols.get("boat")),
                        "type": self.get_cell_text(datos_barco, cols.get("type")),
                        "mna": self.get_cell_text(datos_barco, cols.get("mna")),

                        # 👇 aquí metes la magia
                        "owner": owner,
                        "club": club,
                    }

                    datos.append(fila_datos)

                self.logger.info(f"[OK] Table {table_idx} processed ({len(filas)} rows)")

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing table {table_idx}: {e}", exc_info=True)

        self.logger.info(f"[INFO] Total boats scraped: {len(datos)}")

        return datos


def scrape(url, browser):
    scraper = SportspageScraper()
    return scraper.run(url, browser)
