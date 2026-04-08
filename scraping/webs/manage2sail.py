import pandas as pd

from app.core.base_scraper import BaseScraper


class Manage2SailScraper(BaseScraper):

    def __init__(self):
        super().__init__("manage2sail")


    def scrape(self, url, browser):
        df = pd.DataFrame()

        page = browser.new_page()

        self.logger.info(f"[STEP] Scraping URL: {url}")

        if url:
            try:
                page.goto(url)

                event_id = self.extract_event_id(url)

                class_ids = self.get_class_ids(page)

                all_data = []

                for cls in class_ids:
                    class_id = cls["class_id"]

                    data_json = self.get_class_results(page, event_id, class_id)

                    if data_json:
                        rows = self.obtener_datos(data_json)
                        all_data.extend(rows)

                if all_data:
                    df = pd.DataFrame(all_data)

                    self.logger.info(f"[OK] Scraped {len(df)} rows")

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


    def extract_event_id(self, url):
        event_id = url.split("/event/")[1].split("/")[0].replace("#!", "")

        return event_id

    def get_class_ids(self, page):
        self.logger.info("[STEP] Discovering class IDs via interaction")

        class_ids = set()

        def handle_response(response):
            try:
                url = response.url

                if "/regattaresult/" in url:
                    class_id = url.split("/regattaresult/")[1]
                    class_ids.add(class_id)

            except:
                pass

        page.on("response", handle_response)

        page.reload()
        
        page.wait_for_timeout(2000)

        page.remove_listener("response", handle_response)

        result = [{"class_id": cid} for cid in class_ids]

        self.logger.info(f"[OK] Found {len(class_ids)} class IDs")

        return result

    def get_class_results(self, page, event_id, class_id):
        url = f"https://manage2sail.com/api/event/{event_id}/regattaresult/{class_id}"

        data = self.get_json_with_playwright(page, url)

        return data

    def get_json_with_playwright(self, page, url):
        try:
            response = page.request.get(url)

            if response.status != 200:
                self.logger.warning(f"[WARN] Status {response.status} for {url}")
                return None

            return response.json()

        except Exception as e:
            self.logger.error(f"[FAIL] Error loading JSON {url}: {e}", exc_info=True)
            return None
        
    def obtener_datos(self, data):
        rows = []

        class_name = data.get("RegattaName")

        for entry in data.get("EntryResults", []):

            boat_owner = entry.get("BoatOwner")
            name = entry.get("TeamName")

            if not boat_owner or boat_owner.strip() == "":
                boat_owner = name

            row = {
                "class": class_name,

                "sail_number": entry.get("SailNumber"),
                "boat_name": entry.get("BoatName") or None,
                "boat_type": entry.get("BoatType"),
                "club": entry.get("ClubName"),

                "boat_owner": boat_owner.title()
            }

            rows.append(row)

        return rows

def scrape(url, browser):
    scraper = Manage2SailScraper()
    return scraper.run(url, browser)
