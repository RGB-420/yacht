import requests
import pandas as pd
from urllib.parse import urljoin

from app.core.base_scraper import BaseScraper


class CowesClassicScraper(BaseScraper):

    def __init__(self):
        super().__init__("cowes_classic")


    def scrape(self, url, browser):
        df = pd.DataFrame()
        page = browser.new_page()

        self.logger.info(f"[STEP] Scraping main URL: {url}")

        try:
            links = self.obtener_links_resultados(page, url)

            self.logger.info(f"[INFO] Found {len(links)} result links")

            for link in links:
                try:
                    self.logger.info(f"[STEP] Processing: {link['title']}")

                    data = self.obtener_datos(page, link['url'], link['title'])

                    if data:
                        df_temp = pd.DataFrame(data)
                        df = pd.concat([df, df_temp], ignore_index=True)

                        self.logger.info(f"[OK] {len(df_temp)} rows scraped")

                    else:
                        self.logger.warning(f"[EMPTY] No data found for {link['title']}")

                except Exception as e:
                    self.logger.error(f"[FAIL] Error processing {link['url']}: {e}", exc_info=True)

        except Exception as e:
            self.logger.error(f"[FAIL] Error in scrape(): {e}", exc_info=True)
            return None

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


    def obtener_html(self, session, URL):
        try:
            response = session.get(URL, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"[FAIL] Error fetching {URL}: {e}")
            return None


    def obtener_links_resultados(self, page, base_url):
        page.goto(base_url)
        page.wait_for_selector("table")

        links = []

        anchors = page.locator(
            "table.com-content-category__table tbody th.list-title a"
        )

        count = anchors.count()

        self.logger.info(f"[INFO] Found {count} anchors")

        for i in range(count):
            href = anchors.nth(i).get_attribute("href")
            title = anchors.nth(i).inner_text().strip()

            if not href:
                continue

            title_clean = (
                title
                .replace("Racing Results for Cowes Classics Regatta 2025", "")
                .strip()
            )

            full_url = urljoin(base_url, href)

            links.append({
                "url": full_url,
                "title": title_clean
            })

        return links


    def get_column_map(self, table):
        header_row = table.locator("thead tr").first
        header_cells = header_row.locator("th")

        col_map = {}

        for i in range(header_cells.count()):
            text = header_cells.nth(i).inner_text().strip().lower()

            if "boat" in text:
                col_map["Name"] = i
            elif "sail number" in text or "sailno" in text or "sail no." in text:
                col_map["SailNo"] = i
            elif "design" in text:
                col_map["Type"] = i

        self.logger.info(f"[INFO] Column map: {col_map}")

        return col_map


    def obtener_datos(self, page, url: str, clase):
        self.logger.info(f"[STEP] Loading result page: {url}")

        page.goto(url)
        page.wait_for_timeout(3000)

        table = page.locator("table").first
        rows = table.locator("tbody tr")

        col_map = self.get_column_map(table)

        boats = []

        for r in range(rows.count()):
            row = rows.nth(r)
            cells = row.locator("td")

            if cells.count() == 0:
                continue

            sailno = (
                cells.nth(col_map["SailNo"]).inner_text().strip()
                if "SailNo" in col_map else None
            )
            
            name = (
                cells.nth(col_map["Name"]).inner_text().strip()
                if "Name" in col_map else None
            )

            type_ = (
                cells.nth(col_map["Type"]).inner_text().strip()
                if "Type" in col_map else None
            )

            boats.append({
                "Boat Number": sailno,
                "Name": name,
                "Class": clase,
                "Type": type_
            })

        self.logger.info(f"[OK] Extracted {len(boats)} rows from {clase}")

        return boats


def scrape(url, browser):
    scraper = CowesClassicScraper()
    return scraper.run(url, browser)