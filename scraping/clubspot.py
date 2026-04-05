import pandas as pd
from bs4 import BeautifulSoup
import re
import requests

from app.core.base_scraper import BaseScraper


class ClubSpotScraper(BaseScraper):

    def __init__(self):
        super().__init__("clubspot")

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


    def get_column_map(self, page, headers):
        col_map = {}
        
        for i in range(headers.count()):
            th = headers.nth(i)
            text = th.inner_text().strip()

            if text.startswith("Race"):
                col_map[text] = i
                continue

            if text:
                col_map[text] = i

        self.logger.info(f"[INFO] Column map: {list(col_map.keys())}")

        return col_map


    def get_valid_table(self, page):
        tables = page.locator("#table-container table")
        count = tables.count()

        for i in range(count):
            table = tables.nth(i)

            has_tbody = table.locator("tbody").count() > 0
            rows = table.locator("tbody tr:visible")

            if has_tbody and rows.count() > 0:
                self.logger.info(f"[INFO] Valid table found (index {i})")
                return table

        self.logger.warning("[WARNING] No valid table found")
        return None


    def obtener_datos(self, page, url):
        self.logger.info("[STEP] Loading page")

        page.goto(url)
        page.wait_for_load_state("domcontentloaded")

        boats = []

        selects = page.locator("select")
        select = selects.nth(0)

        options = select.locator("option:not(.text-danger)")

        count = options.count()
        self.logger.info(f"[INFO] Found {count} classes")

        for opt_idx in range(count):
            try:
                option = options.nth(opt_idx)
                value = option.get_attribute("value")
                clase = option.inner_text().strip()

                self.logger.info(f"[CLASS] Processing class: {clase} ({value})")
                
                select.select_option(value=value)
                page.wait_for_selector("tr.resultsRow", timeout=10000)

                table = self.get_valid_table(page)

                if table is None:
                    self.logger.warning(f"[SKIP] No valid table for class {clase}")
                    continue

                headers = table.locator("tr.tableHeaderRow th")
                rows = table.locator("tr.resultsRow")

                col_map = self.get_column_map(page, headers)

                for row_idx in range(rows.count()):
                    row = rows.nth(row_idx)
                    cells = row.locator("td")

                    def safe_cell(cells, col_map, key):
                        idx = col_map.get(key)
                        if idx is None:
                            return None

                        cell_count = cells.count()

                        if idx >= cell_count:
                            return None

                        return cells.nth(idx).inner_text().strip()
                        
                    boats.append({
                        "sail_number": safe_cell(cells, col_map, "SAIL NUMBER"),
                        "boat_name": safe_cell(cells, col_map, "BOAT NAME"),
                        "type": safe_cell(cells, col_map, "BOAT TYPE"),
                        "owner": safe_cell(cells, col_map, "SAILORS"),
                        "club": safe_cell(cells, col_map, "CLUB/ORG"),
                        "class": clase,
                    })

                self.logger.info(f"[OK] {rows.count()} rows scraped for class {clase}")

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing class {clase}: {e}", exc_info=True)

        self.logger.info(f"[INFO] Total boats scraped: {len(boats)}")

        return boats


def scrape(url, browser):
    scraper = ClubSpotScraper()
    return scraper.run(url, browser)
