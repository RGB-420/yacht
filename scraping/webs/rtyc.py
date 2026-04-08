import pandas as pd
from bs4 import BeautifulSoup

from app.core.base_scraper import BaseScraper


COLUMN_MAP = {
    "division": "Fleet",
    "sailno": "SailNo",
    "boat": "Boat",
    "class": "Class",
    "club": "Club",
}


class RTYCScraper(BaseScraper):

    def __init__(self):
        super().__init__("rtyc")


    def scrape(self, url, browser):
        df = pd.DataFrame()
        page = browser.new_page()

        self.logger.info(f"[STEP] Scraping URL: {url}")

        try:
            links = self.get_all_links(page, url)
            self.logger.info(f"[INFO] Found {len(links)} links")

            for link in links:
                try:
                    self.logger.info(f"[STEP] Processing link: {link}")

                    html = self.get_html_with_playwright(page, link)

                    if html:
                        data = self.obtener_barcos(html)

                        if data:
                            df_temp = pd.DataFrame(data)
                            df = pd.concat([df, df_temp], ignore_index=True)

                            self.logger.info(f"[OK] {len(df_temp)} rows scraped")

                        else:
                            self.logger.warning(f"[EMPTY] No boats found for {link}")

                    else:
                        self.logger.warning(f"[SKIP] Could not load HTML: {link}")

                except Exception as e:
                    self.logger.error(f"[FAIL] Error processing link {link}: {e}", exc_info=True)

        except Exception as e:
            self.logger.error(f"[FAIL] Error in scrape(): {e}", exc_info=True)
            return None

        df = df.drop_duplicates(subset=['sailno', 'boat'], keep="first")

        return df


    def get_all_links(self, page, url):
        html = self.get_html_with_playwright(page, url)

        if not html:
            self.logger.warning("[SKIP] Could not load main page")
            return []

        soup = BeautifulSoup(html, "html.parser")

        tablas = soup.find_all("table", class_="has-fixed-layout")

        if not tablas:
            self.logger.warning("[SKIP] No tables found for links")
            return []

        links = [
            a["href"]
            for a in tablas[0].find_all("a", href=True)
        ]

        return links


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

        tablas = soup.find_all("table", class_="summarytable")
        titles = soup.find_all("h3", class_="summarytitle")

        self.logger.info(f"[INFO] Tables found: {len(tablas)}")

        datos = []

        for i, tabla in enumerate(tablas):
            try:
                raw_title = titles[i].get_text(strip=True) if i < len(titles) else None
                table_title = raw_title.replace(" Fleet", "").strip() if raw_title else None

                self.logger.info(f"[STEP] Processing table {i} ({table_title})")

                indices = self.get_column_indices(tabla)
                cols = {k: indices.get(v) for k, v in COLUMN_MAP.items()}

                filas = tabla.find("tbody").find_all("tr")

                for fila in filas:
                    datos_barco = fila.find_all("td")

                    fila_datos = {
                        key: self.get_cell_text(datos_barco, idx)
                        for key, idx in cols.items()
                    }

                    if not fila_datos.get("division"):
                        fila_datos["division"] = table_title

                    datos.append(fila_datos)

                self.logger.info(f"[OK] Table {i} processed ({len(filas)} rows)")

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing table {i}: {e}", exc_info=True)

        self.logger.info(f"[INFO] Total boats scraped: {len(datos)}")

        return datos


def scrape(url, browser):
    scraper = RTYCScraper()
    return scraper.run(url, browser)