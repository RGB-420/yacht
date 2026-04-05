import pandas as pd
import numpy as np

from app.core.base_scraper import BaseScraper


#---------- CONFIGURATION ----------
all_regatas = True
selected_regatas = []
#-----------------------------------


class ArchiveHalsailScraper(BaseScraper):

    def __init__(self):
        super().__init__("archive_halsail")

    def scrape(self, url, browser):
        df = pd.DataFrame()

        self.logger.info(f"[STEP] Scraping URL: {url}")

        page = browser.new_page()
            
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

        # Cleaning
        df = df.replace(r'^\s*$', np.nan, regex=True)
        df = df[df.apply(lambda row: any(pd.notnull(v) for v in row), axis=1)]
        df = df.drop_duplicates()
        df = df.where(pd.notnull(df), None)

        if all_regatas:
            return df
        else:
            df = df[df["class"].isin(selected_regatas)]
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

        self.logger.info(f"[INFO] Column map detected: {list(col_map.keys())}")

        return col_map


    def get_valid_table(self, page):
        tables = page.locator("#divResults table:not([id])")
        count = tables.count()

        for i in range(count):
            table = tables.nth(i)

            has_thead = table.locator("thead").count() > 0
            has_tbody = table.locator("tbody").count() > 0
            rows = table.locator("tbody tr:visible")

            if has_thead and has_tbody and rows.count() > 0:
                self.logger.info(f"[INFO] Valid table found (index {i})")
                return table

        self.logger.warning("[WARNING] No valid table found")
        return None


    def obtener_datos(self, page, url):
        self.logger.info("[STEP] Loading page")

        page.goto(url)
        page.wait_for_load_state("domcontentloaded")

        boats = []

        select = page.locator("#ddClass")
        options = select.locator("option:not(.text-danger)")

        self.logger.info(f"[INFO] Found {options.count()} classes")

        for opt_idx in range(options.count()):
            try:
                option = options.nth(opt_idx)
                value = option.get_attribute("value")
                clase = option.inner_text().strip()

                self.logger.info(f"[CLASS] Processing class: {clase} ({value})")

                # change class
                page.select_option("#ddClass", value=value)
                page.wait_for_timeout(8000)

                table = self.get_valid_table(page)

                if table is None:
                    self.logger.warning(f"[SKIP] No table for class {clase}")
                    continue

                headers = table.locator("thead tr th")
                rows = table.locator("tbody tr:visible")

                col_map = self.get_column_map(page, headers)

                for row_idx in range(rows.count()):
                    row = rows.nth(row_idx)
                    cells = row.locator("td")

                    def safe_cell(cells, col_map, key):
                        idx = col_map.get(key)
                        if idx is None:
                            return None
                        if idx >= cells.count():
                            return None
                        return cells.nth(idx).inner_text().strip()
                    
                    boats.append({
                        "sail_number": safe_cell(cells, col_map, "Sail Number"),
                        "boat_name": safe_cell(cells, col_map, "Name"),
                        "type": safe_cell(cells, col_map, "Type"),
                        "owner": safe_cell(cells, col_map, "Owner"),
                        "club": safe_cell(cells, col_map, "Club"),
                        "class": clase,
                    })

                self.logger.info(f"[OK] {rows.count()} rows scraped for class {clase}")

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing class {clase}: {e}", exc_info=True)

        self.logger.info(f"[INFO] Total boats scraped: {len(boats)}")

        return boats


def scrape(url, browser):
    scraper = ArchiveHalsailScraper()
    return scraper.run(url, browser)