import pandas as pd
import re

from app.core.base_scraper import BaseScraper


#---------- CONFIGURATION ----------
COLUMN_ALIASES = {
    "sail_number": ["SAIL #", "VELA", "Sail No", "Sail Number"],
    "boat_name": ["SPONSOR/BOAT", "SPONSOR/BARCO", "Boat Name", "Yacht"],
    "owner": ["CREW", "TRIPULANTES", "Helm", "Skipper"],
    "club": ["CLUB", "Club", "Yacht Club"]
}
#-----------------------------------


class SailtiScraper(BaseScraper):

    def __init__(self):
        super().__init__("sailti")


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

        df = df.explode("club")

        df = df.drop_duplicates()

        return df

    def get_column_map(self, page, headers):
        raw_map = {}

        for i in range(headers.count()):
            text = headers.nth(i).inner_text().strip().upper()

            if text:
                raw_map[text] = i

        col_map = {}

        for key, aliases in COLUMN_ALIASES.items():
            for alias in aliases:
                alias = alias.upper()
                if alias in raw_map:
                    col_map[key] = raw_map[alias]
                    break  # cogemos el primero que coincida

        self.logger.info(f"[INFO] Column map: {col_map}")

        return col_map


    def get_valid_table(self, page):
        table = page.locator("table#myTable_, table#myTable")

        if table.count() == 0:
            self.logger.warning("[WARNING] Table not found")
            return None

        rows = table.locator("tbody tr")

        if rows.count() == 0:
            self.logger.warning("[WARNING] Table has no rows")
            return None

        return table
    
    def safe_cell(self, cells, col_map, key, mode=None, transform=None):
        idx = col_map.get(key)
        if idx is None or idx >= cells.count():
            return None

        try:
            text = cells.nth(idx).inner_text().strip()
            text = text.replace("\n\n", "\n").replace("  ", " ")

            if not text:
                return None

            if mode == "multi":
                lines = []
                for line in text.split("\n"):
                    parts = re.split(r"[,/]", line)
                    for part in parts:
                        part = part.strip()
                        if part:
                            lines.append(part)

                text = " / ".join(dict.fromkeys(lines)) 

            elif mode == "first":
                text = text.split("\n")[0].strip()

            if transform and isinstance(text, str):
                text = transform(text)

            return text

        except:
            return None

    def obtener_datos(self, page, url):
        self.logger.info("[STEP] Loading page")

        page.goto(url)
        page.wait_for_load_state("domcontentloaded")

        boats = []

        page.wait_for_selector("#resultsall-container", state="attached")

        buttons_row = page.locator("#resultsall-container").locator("div.row")

        total = buttons_row.locator("a").count()
        self.logger.info(f"[INFO] Found {total} classes")

        for i in range(total):
            try:
                buttons = page.locator("a.ico-sailclass")
                btn = buttons.nth(i)

                clase = btn.locator("svg g").first.get_attribute("id")
                clase = clase.replace("-", " ").upper()

                class_attr = btn.get_attribute("class")

                self.logger.info(f"[CLASS] Processing class: {clase}")

                btn.scroll_into_view_if_needed()
                btn.click(force=True)

                page.wait_for_timeout(10000)

                table = self.get_valid_table(page)

                if table is None:
                    self.logger.warning(f"[SKIP] No valid table for class {clase}")
                    continue

                headers = table.locator("thead tr th")
                rows = table.locator("tbody tr")

                col_map = self.get_column_map(page, headers)

                for row_idx in range(rows.count()):
                    row = rows.nth(row_idx)
                    cells = row.locator("td")

                    boats.append({
                        "sail_number": self.safe_cell(cells, col_map, "sail_number"),
                        "boat_name": self.safe_cell(cells, col_map, "boat_name"),
                        "owner": self.safe_cell(cells, col_map, "owner", mode="first", transform=str.title),
                        "club": self.safe_cell(cells, col_map, "club", mode="multi"),
                        "class": clase,
                    })

                self.logger.info(f"[OK] {rows.count()} rows scraped for class {clase}")

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing class {clase}: {e}", exc_info=True)

        self.logger.info(f"[INFO] Total boats scraped: {len(boats)}")

        return boats


def scrape(url, browser):
    scraper = SailtiScraper()
    return scraper.run(url, browser)