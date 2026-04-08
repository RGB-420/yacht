import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from app.core.base_scraper import BaseScraper


class Cape31Scraper(BaseScraper):

    def __init__(self):
        super().__init__("cape31")


    def scrape(self, url, browser):
        df = pd.DataFrame()
        page = browser.new_page()

        self.logger.info(f"[STEP] Scraping URL: {url}")

        if url:
            try:
                data = self.obtener_datos(page, url)

                if data:
                    df_temp = pd.DataFrame(data)
                    df = pd.concat([df, df_temp], ignore_index=True)

                    self.logger.info(f"[OK] Scraped {len(df_temp)} rows")

                else:
                    self.logger.warning("[EMPTY] No data found")

            except Exception as e:
                self.logger.error(f"[FAIL] Error in scrape(): {e}", exc_info=True)
                return None
        else:
            self.logger.error("[FAIL] Invalid URL")
            return None

        df = df.drop_duplicates()

        return df


    def set_page_index(self, url, page):
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        qs["page"] = [str(page)]
        new_query = urlencode(qs, doseq=True)
        return urlunparse(parsed._replace(query=new_query))


    def get_page_indices(self, html):
        soup = BeautifulSoup(html, "html.parser")

        pagination = soup.find("ul", class_="pagination")
        if not pagination:
            self.logger.info("[INFO] Single page detected")
            return [1]

        indices = set()

        for a in pagination.find_all("a", href=True):
            parsed = urlparse(a["href"])
            qs = parse_qs(parsed.query)

            if "page" in qs:
                try:
                    indices.add(int(qs["page"][0]))
                except ValueError:
                    pass

        indices = sorted(indices) if indices else [1]

        self.logger.info(f"[INFO] Found pages: {indices}")

        return indices


    def get_html_with_playwright(self, page, url: str) -> str:
        try:
            page.goto(url)
            page.wait_for_load_state("networkidle")
            return page.content()
        except Exception as e:
            self.logger.error(f"[FAIL] Error loading page {url}: {e}", exc_info=True)
            return None


    def obtener_datos(self, page, url: str):
        self.logger.info("[STEP] Loading initial page")

        page.goto(url)
        page.wait_for_timeout(2000)

        html = self.get_html_with_playwright(page, url)

        if not html:
            self.logger.error("[FAIL] Could not load HTML")
            return []

        page_indices = self.get_page_indices(html)

        boats = []

        for page_index in page_indices:
            try:
                page_url = self.set_page_index(url, page_index)

                self.logger.info(f"[STEP] Processing page {page_index}")

                page.goto(page_url)

                table = page.locator("table")

                table_count = table.count()
                self.logger.info(f"[INFO] Tables found: {table_count}")

                rows = table.locator("tbody tr")
                row_count = rows.count()

                self.logger.info(f"[INFO] Rows found: {row_count}")

                for i in range(row_count):
                    row = rows.nth(i)
                    cells = row.locator("td")

                    if cells.count() < 4:
                        continue

                    boat_name = cells.nth(1).inner_text().strip()
                    sail_number = cells.nth(2).inner_text().strip()
                    owner = cells.nth(3).inner_text().strip()

                    boats.append({
                        "boat_name": boat_name,
                        "sail_number": sail_number,
                        "owner": owner
                    })

                self.logger.info(f"[OK] Page {page_index} processed")

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing page {page_index}: {e}", exc_info=True)

        self.logger.info(f"[INFO] Total boats scraped: {len(boats)}")

        return boats


# 🔥 Wrapper para tu runner
def scrape(url, browser):
    scraper = Cape31Scraper()
    return scraper.run(url, browser)