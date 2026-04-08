import pandas as pd
from urllib.parse import urljoin

from app.core.base_scraper import BaseScraper


base_url = "https://www.cowesweek.co.uk/web/code/php/"

FIELDS = ['sail_number', 'entered_by', 'design_type']


class CowesWeekScraper(BaseScraper):

    def __init__(self):
        super().__init__("cowes_week")


    def scrape(self, url, browser):
        df = pd.DataFrame()

        page = browser.new_page()

        self.logger.info(f"[STEP] Scraping URL: {url}")

        try:
            values = self.get_all_select_values(page, url)

            self.logger.info(f"[INFO] Found {len(values)} selector values")

            for value in values:
                try:
                    self.logger.info(f"[STEP] Processing selector value: {value}")

                    self.go_to_selector(page, url, value)

                    links_boats = self.obtener_links_barcos(page)

                    self.logger.info(f"[INFO] Found {len(links_boats)} boat links")

                    for link in links_boats:
                        try:
                            self.logger.info(f"[STEP] Processing boat URL: {link}")

                            data = self.obtener_datos_barcos(page, link)

                            if data:
                                df_temp = pd.DataFrame([data])
                                df = pd.concat([df, df_temp], ignore_index=True)

                            else:
                                self.logger.warning(f"[EMPTY] No data found for {link}")

                        except Exception as e:
                            self.logger.error(f"[FAIL] Error processing boat {link}: {e}", exc_info=True)

                except Exception as e:
                    self.logger.error(f"[FAIL] Error processing selector {value}: {e}", exc_info=True)

        except Exception as e:
            self.logger.error(f"[FAIL] Error in scrape(): {e}", exc_info=True)
            return None

        df = df.drop_duplicates()
        df = df.rename(columns={'entered_by': 'owner', 'design_type': 'type'})

        return df


    def get_all_select_values(self, page, url):
        page.goto(url)
        page.wait_for_load_state("networkidle")

        values = page.eval_on_selector_all(
            "select[name='resultrequest'] option",
            "options => options.map(o => o.value).filter(v => v !== '0')"
        )

        return values


    def go_to_selector(self, page, url, value):
        page.goto(url)
        page.wait_for_load_state("networkidle")

        page.select_option("select[name='resultrequest']", value=value)
        page.click("button[name='submit']")

        page.wait_for_selector("div.resultspage table")


    def obtener_links_barcos(self, page):
        rows = page.locator("div.resultspage table tr").all()

        data = []

        for row in rows[1:]:
            cells = row.locator("td")
            if cells.count() < 2:
                continue

            link = cells.nth(1).locator("a")
            if link.count() == 0:
                continue

            href = link.get_attribute("href")
            full_url = urljoin(base_url, href)

            data.append(full_url)

        return data


    def obtener_datos_barcos(self, page, url):
        page.goto(url)

        if not page.locator("div.two-thirds").count():
            self.logger.warning(f"[SKIP] Empty page: {url}")
            return None

        data = {}

        try:
            h3 = page.locator("div.two-thirds h3")
            data["boat_name"] = h3.evaluate(
                "el => el.childNodes[0].textContent.trim()"
            )
            data["boat_class"] = h3.locator("span").inner_text().strip()
        except Exception:
            self.logger.warning(f"[WARNING] Incomplete header: {url}")

        table = page.locator("div.two-thirds table.SearchDetails")

        if table.count():
            rows = table.locator("tbody tr")

            for i in range(rows.count()):
                row = rows.nth(i)
                cells = row.locator("td")

                if cells.count() < 2:
                    continue

                key = cells.nth(0).inner_text().strip()
                value = cells.nth(1).inner_text().strip()

                key = key.lower().replace(" ", "_")

                if key in FIELDS:
                    data[key] = value
        else:
            self.logger.warning(f"[SKIP] No details table: {url}")

        if not data:
            return None

        return data


def scrape(url, browser):
    scraper = CowesWeekScraper()
    return scraper.run(url, browser)