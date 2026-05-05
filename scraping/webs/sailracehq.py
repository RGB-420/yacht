import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse
import re

from app.core.base_scraper import BaseScraper


BASE_DOMAIN = "https://sailracehq.com/"


class SailRaceHQScraper(BaseScraper):

    def __init__(self):
        super().__init__("sailracehq")
        self.club_cache = {}


    def scrape(self, url, browser):
        try:
            LINKS = []

            page = browser.new_page()

            self.logger.info(f"[STEP] Processing URL: {url}")

            link_type = self.get_link_type(url)
            self.logger.info(f"[INFO] Link type: {link_type}")

            if link_type == "race_results":
                LINKS.append(url)

            elif link_type == "event_results":
                page.goto(url, wait_until="domcontentloaded")
                race_links = self.get_race_results_from_event(page)
                self.logger.info(f"[INFO] Race links found: {len(race_links)}")
                LINKS.extend(race_links)

            else:
                self.logger.warning("[SKIP] Unknown link type")
                return pd.DataFrame()
            
            rows = []

            for LINK in LINKS:
                try:
                    self.logger.info(f"[STEP] Processing race link: {LINK}")

                    page.close()
                    page = browser.new_page()
                    page.goto(LINK)

                    CLASSES = self.get_tabs_from_tablist(page, BASE_DOMAIN)

                    for target in CLASSES:
                        if target["division"] == "#Tags":
                            continue

                        if "Line Honours" in target["division"]:
                            continue

                        division = target["division"]
                        base_url = target["url"]

                        self.logger.info(f"[CLASS] Division: {division}")

                        html = self.get_html_with_playwright(page, base_url)

                        if not html:
                            self.logger.warning(f"[SKIP] No HTML for {base_url}")
                            continue

                        soup = BeautifulSoup(html, "html.parser")

                        subclasses = self.get_subclasses_from_page(soup)

                        irc_overall = [s for s in subclasses if s["subclass_name"] == "IRC Overall"]

                        if irc_overall:
                            subclasses = irc_overall
                        elif not subclasses:
                            subclasses = [{"subclass_name": None, "url": base_url}]

                        for sub in subclasses:
                            subclass_name = sub["subclass_name"]
                            sub_url = sub["url"]

                            self.logger.info(f"[SUBCLASS] {subclass_name}")

                            html = self.get_html_with_playwright(page, sub_url)
                            soup = BeautifulSoup(html, "html.parser")

                            page_indices = self.get_page_indices(soup)
                            self.logger.info(f"[INFO] Pages: {len(page_indices)}")

                            for page_index in page_indices:
                                try:
                                    page_url = self.set_page_index(sub_url, page_index)
                                    self.logger.info(f"[STEP] Page {page_index}")

                                    html = self.get_html_with_playwright(page, page_url)
                                    soup = BeautifulSoup(html, "html.parser")

                                    accordion = soup.find("div", id="accordion")
                                    if not accordion:
                                        self.logger.warning("[SKIP] No accordion found")
                                        continue

                                    boats = accordion.find_all("ul", class_="rz-datalist-data")
                                    self.logger.info(f"[INFO] Boats found: {len(boats)}")
                                    
                                    for ul in boats:
                                        boat_data = self.extract_boat_data(ul)
                                        boat_data["class_name"] = division

                                        if boat_data:
                                            rows.append(boat_data)

                                except Exception as e:
                                    self.logger.error(f"[FAIL] Error in page {page_index}: {e}", exc_info=True)

                except Exception as e:
                    self.logger.error(f"[FAIL] Error processing race link {LINK}: {e}", exc_info=True)

            self.logger.info(f"[ENRICH] Preparing club extraction")

            club_map = self.build_club_map(rows, browser)
            rows = self.apply_club_map(rows, club_map)

            df = pd.DataFrame(rows)

            df = df.drop_duplicates(subset=["boat_name", "sail_number"])
            df = df[['boat_name', 'sail_number', 'owner', 'boat_type', 'class_name', 'club']]

            return df
        
        finally:
            page.close()


    def get_link_type(self, url):
        path = urlparse(url).path.lower()

        if path.startswith("/raceresults"):
            return "race_results"

        if path.startswith("/results/event"):
            return "event_results"

        return "unknown"


    def get_race_results_from_event(self, page):
        page.wait_for_load_state("networkidle")

        soup = BeautifulSoup(page.content(), "html.parser")

        links = set()

        for a in soup.find_all("a", href=True):
            if "/raceresults/" in a["href"]:
                links.add(urljoin(BASE_DOMAIN, a["href"]))

        return sorted(links)


    def set_page_index(self, url, page_index, page_size=25):
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)

        qs["pageIndex"] = [str(page_index)]
        qs["method"] = ["PageChanged"]
        qs["pageSize"] = [str(page_size)]

        return urlunparse(parsed._replace(query=urlencode(qs, doseq=True)))


    def get_page_indices(self, soup):
        pagination = soup.find("ul", class_="pagination")

        if not pagination:
            return [0]

        indices = []

        page_items = pagination.find_all("li", class_="page-item-number")

        for li in page_items:
            a = li.find("a", href=True)
            if not a:
                continue

            qs = parse_qs(urlparse(a["href"]).query)

            if "pageIndex" in qs:
                try:
                    idx = int(qs["pageIndex"][0])
                    indices.append(idx)
                except:
                    pass

        return sorted(indices) if indices else [0]


    def extract_boat_data(self, ul):
        data = {}

        name_tag = ul.select_one("a.btn-view-boat")
        data["boat_name"] = name_tag.get_text(strip=True) if name_tag else None
        data["boat_link"] = name_tag.get("href") if name_tag else None

        sail_tag = ul.select_one(".bow-number") or ul.select_one("span[style*='font-size']")
        data["sail_number"] = sail_tag.get_text(strip=True) if sail_tag else None

        details = ul.select_one(".li-row-2")

        if details:
            def get_detail(label):
                label_div = details.find("div", string=lambda x: x and label in x)
                value_div = label_div.find_next("div", class_="small") if label_div else None
                return value_div.get_text(strip=True) if value_div else None

            data["owner"] = get_detail("Owner")
            data["boat_type"] = get_detail("Boat Type")

        else:
            data["owner"] = None
            data["boat_type"] = None

        return data


    def extract_club(self, boat_data, page):
        key = (boat_data.get("boat_name"), boat_data.get("sail_number"))
        self.logger.info(f"[CLUB] Fetching club for {boat_data.get('boat_name')}")

        if key in self.club_cache:
            self.logger.info(f"[CACHE] Using cached club for {key}")
            boat_data["club"] = self.club_cache[key]
            return boat_data

        link = boat_data.get("boat_link")

        if not link:
            boat_data["club"] = None
            return boat_data

        try:
            url = urljoin(BASE_DOMAIN, boat_data["boat_link"])

            page.goto(url, wait_until="domcontentloaded", timeout=10000)
            page.wait_for_selector("div.col-lg-4", timeout=5000)

            club_locator = page.locator("div.col-lg-4", has_text=re.compile("club", re.I))

            if club_locator.count():
                club = (
                    club_locator
                    .locator("..")
                    .locator("div.col.font-weight-bold")
                    .first
                    .inner_text()
                    .strip()
                )
            else:
                club = None

            boat_data["club"] = club
            if club:
                self.club_cache[key] = club

        except Exception as e:
            self.logger.warning(f"[WARNING] Error extracting club: {e}")
            boat_data["club"] = None

        return boat_data


    def get_html_with_playwright(self, page, url):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=10000)
            page.wait_for_load_state("networkidle")
            return page.content()
        except Exception as e:
            self.logger.error(f"[FAIL] Error loading {url}: {e}", exc_info=True)
            return None


    def get_subclasses_from_page(self, soup):
        ul = soup.find("ul", class_="classes-wrapper")
        if not ul:
            return []

        return [
            {"subclass_name": a.get_text(strip=True), "url": a["href"]}
            for a in ul.find_all("a", href=True)
        ]


    def get_tabs_from_tablist(self, page, base_domain):
        page.wait_for_selector("ul.rz-tabview-nav li")

        tabs = page.query_selector_all("ul.rz-tabview-nav li")
        classes = []

        for tab in tabs:
            link = tab.query_selector("a.rz-tabview-nav-link")
            name_el = tab.query_selector("span.rz-tabview-title")

            if not link or not name_el:
                continue

            onclick = link.get_attribute("onclick")

            if not onclick:
                continue

            match = re.search(r'window.location\s*=\s*"([^"]+)"', onclick)
            if not match:
                continue

            classes.append({
                "division": name_el.inner_text().strip(),
                "url": base_domain + match.group(1)
            })

        return classes
    
    def deduplicate_boats(self, rows):
        self.logger.info(f"[DEDUP] Reducing boats before club extraction")

        unique_boats = {}

        for row in rows:
            key = (row["boat_name"], row["sail_number"])
            if key not in unique_boats:
                unique_boats[key] = row

        unique_rows = list(unique_boats.values())

        self.logger.info(f"[DEDUP] {len(rows)} -> {len(unique_rows)} unique boats")

        return unique_rows
    

    def enrich_clubs_sequential(self, rows, browser):
        self.logger.info(f"[ENRICH] Extracting clubs sequentially ({len(rows)} boats)")

        club_page = browser.new_page()

        for i, row in enumerate(rows):
            if i % 50 == 0:
                self.logger.info(f"[ENRICH] Progresss: {i}/{len(rows)}")

            rows[i] = self.extract_club(row, club_page)

        club_page.close()

        return rows
    
    def map_clubs_back(self, original_rows, enriched_rows):
        club_map = {
            (row["boat_name"], row["sail_number"]): row.get("club")
            for row in enriched_rows
        }

        for row in original_rows:
            key = (row["boat_name"], row["sail_number"])
            row["club"] = club_map.get(key)

        return original_rows

    def build_boat_key(self, row):
        name = (row.get("boat_name") or "").strip().lower()
        sail = (row.get("sail_number") or "").replace(" ", "").upper()
        return (name, sail)
    

    def build_club_map(self, rows, browser):
        self.logger.info(f"[ENRICH] Building club map from {len(rows)} rows")

        club_page = browser.new_page()
        club_map = {}

        for i, row in enumerate(rows):
            key = self.build_boat_key(row)

            if key in club_map and club_map[key]:
                continue

            enriched = self.extract_club(row, club_page)
            club = enriched.get("club")

            if club:
                club_map[key] = club

        club_page.close()

        return club_map
    
    def apply_club_map(self, rows, club_map):
        for row in rows:
            key = self.build_boat_key(row)
            row["club"] = club_map.get(key)

        return rows


def scrape(url, browser):
    scraper = SailRaceHQScraper()
    return scraper.run(url, browser)