from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

from app.core.base_scraper import BaseScraper


class BurnhamScraper(BaseScraper):

    def __init__(self):
        super().__init__("burnham_week")


    def scrape(self, url, browser):
        df = pd.DataFrame()

        self.logger.info(f"[STEP] Scraping main URL: {url}")

        page = browser.new_page()

        html = self.get_html_with_playwright(page, url)

        if not html:
            self.logger.error("[FAIL] Could not retrieve main HTML")
            return None

        df_links = self.obtener_links(html, base_url=url)

        self.logger.info(f"[INFO] Found {len(df_links)} links")

        for row in df_links.itertuples(index=False):
            try:
                self.logger.info(f"[STEP] Processing URL: {row.url}")

                html = self.get_html_with_playwright(page, row.url)

                if html:
                    data = self.obtener_partidos(html, row.text)

                    if data:
                        df_temp = pd.DataFrame(data)
                        df = pd.concat([df, df_temp], ignore_index=True)

                        self.logger.info(f"[OK] {len(df_temp)} rows scraped from {row.url}")

                    else:
                        self.logger.warning(f"[EMPTY] No data found at {row.url}")

                else:
                    self.logger.warning(f"[SKIP] Could not retrieve HTML from {row.url}")

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing URL {row.url}: {e}", exc_info=True)

        df = df.drop_duplicates()

        return df


    def get_html_with_playwright(self, page, url: str) -> str:
        try:
            page.goto(url)
            page.wait_for_load_state("networkidle")
            return page.content()
        except Exception as e:
            self.logger.error(f"[FAIL] Error loading page {url}: {e}", exc_info=True)
            return None


    def obtener_links(self, html, base_url=None):
        soup = BeautifulSoup(html, "html.parser")

        data = []

        sections = soup.find_all("section", class_="fc_accordion")

        self.logger.info(f"[INFO] Found {len(sections)} sections")

        for seccion in sections:
            for a in seccion.find_all("a", href=True):
                data.append({
                    "url": urljoin(base_url, a["href"]) if base_url else a["href"],
                    "text": a.get_text(strip=True)
                })

        self.logger.info(f"[INFO] Extracted {len(data)} links")

        return pd.DataFrame(data)


    def get_value(self, celdas, col, key):
        idx = col.get(key)
        if idx is None or idx >= len(celdas):
            return None
        return celdas[idx].get_text(strip=True)


    def normalizar_columnas(self, tabla):
        col = {}
        ths = tabla.find("thead").find_all("th")

        for i, th in enumerate(ths):
            name = th.get_text(strip=True)
            name = name.replace("\xa0", "")
            name = name.lower()
            col[name] = i

        self.logger.info(f"[INFO] Normalized columns: {list(col.keys())}")

        return col


    def obtener_partidos(self, html, clase):
        soup = BeautifulSoup(html, "html.parser")
        tablas = soup.find_all("table", class_="summarytable")

        self.logger.info(f"[INFO] Found {len(tablas)} tables for class {clase}")

        datos = []

        for tabla in tablas:
            col = self.normalizar_columnas(tabla)
            filas = tabla.find("tbody").find_all("tr")

            for fila in filas:
                celdas = fila.find_all("td")

                fila_data = {
                    "boat": self.get_value(celdas, col, "boat"),
                    "sailno": self.get_value(celdas, col, "sailno"),
                    "club": self.get_value(celdas, col, "club"),
                    "class": clase,
                    "type": self.get_value(celdas, col, "class"),
                }

                datos.append(fila_data)

        self.logger.info(f"[OK] Extracted {len(datos)} rows for class {clase}")

        return datos


def scrape(url, browser):
    scraper = BurnhamScraper()
    return scraper.run(url, browser)