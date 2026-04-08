from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse
import pandas as pd
import re

from app.core.base_scraper import BaseScraper


BASE_DOMAIN = "https://racing.islandsc.org.uk/"


class RacingIslandsScraper(BaseScraper):

    def __init__(self):
        super().__init__("racing_islands")


    def scrape(self, url, browser):
        df = pd.DataFrame()
        LINKS = []

        page = browser.new_page()

        self.logger.info(f"[STEP] Processing URL: {url}")

        link_type = self.get_link_type(url)
        self.logger.info(f"[INFO] Link type: {link_type}")

        if link_type == "race_results":
            LINKS.append(url)

        elif link_type == "event_results":
            race_links = self.get_race_results_from_event(page)
            self.logger.info(f"[INFO] Race links found: {len(race_links)}")
            LINKS.extend(race_links)

        else:
            self.logger.warning("[SKIP] Unknown link type")
            return pd.DataFrame()

        for LINK in LINKS:
            try:
                self.logger.info(f"[STEP] Processing race link: {LINK}")

                page = browser.new_page()
                page.goto(LINK)

                CLASSES = self.get_tabs_from_tablist(page, BASE_DOMAIN)

                for target in CLASSES:
                    if target["division"] == "#Tags":
                        continue

                    division = target["division"]
                    base_url = target["url"]

                    self.logger.info(f"[CLASS] Division: {division}")

                    html = self.get_html_with_playwright(page, base_url)
                    soup = BeautifulSoup(html, "html.parser")

                    subclasses = self.get_subclasses_from_page(soup)

                    irc_overall = [s for s in subclasses if s["subclass_name"] == "IRC Overall"]
                    isc_overall = [s for s in subclasses if s["subclass_name"] == "ISC Overall"]

                    if irc_overall:
                        subclasses = irc_overall
                    elif isc_overall:
                        subclasses = isc_overall
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
                                    boat_data = self.extract_club(boat_data, page)

                                    if boat_data:
                                        df_temp = pd.DataFrame([boat_data])
                                        df = pd.concat([df, df_temp], ignore_index=True)

                            except Exception as e:
                                self.logger.error(f"[FAIL] Error in page {page_index}: {e}", exc_info=True)

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing race link {LINK}: {e}", exc_info=True)

        df = df.drop_duplicates(subset=["boat_name", "sail_number"])

        df = df[['boat_name', 'sail_number', 'owner', 'boat_type', 'class_name']]

        return df


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

        indices = set()

        for a in pagination.find_all("a", href=True):
            qs = parse_qs(urlparse(a["href"]).query)
            if "pageIndex" in qs:
                try:
                    indices.add(int(qs["pageIndex"][0]))
                except:
                    pass

        return sorted(indices) if indices else [0]


    def extract_boat_data(self, ul):
        data = {}

        name_tag = ul.select_one("a.btn-view-boat")
        data["boat_name"] = name_tag.get_text(strip=True) if name_tag else None
        data["boat_link"] = name_tag.get("href") if name_tag else None

        class_tag = ul.select_one("span[style*='font-size']")
        data["sail_number"] = class_tag.get_text(strip=True) if class_tag else None

        details = ul.find("div", class_="li-row-2")

        if details:
            def get_detail(label):
                label_div = details.find("div", string=lambda x: x and label in x)
                value_div = label_div.find_next("div", class_="small") if label_div else None
                return value_div.get_text(strip=True) if value_div else None

            data["owner"] = get_detail("Owner")
            data["boat_type"] = get_detail("Boat Type")

        return data


    def extract_club(self, boat_data, page):
        if not boat_data.get("boat_link"):
            boat_data["club"] = None
            return boat_data

        try:
            page.goto(BASE_DOMAIN + boat_data["boat_link"])
            page.wait_for_load_state("domcontentloaded")

            club_locator = page.locator("div.col-lg-4", has_text="club")

            if club_locator.count():
                boat_data["club"] = (
                    club_locator
                    .locator("..")
                    .locator("div.col.font-weight-bold")
                    .first
                    .inner_text()
                    .strip()
                )
            else:
                boat_data["club"] = None

        except Exception as e:
            self.logger.warning(f"[WARNING] Error extracting club: {e}")
            boat_data["club"] = None

        return boat_data


    def get_html_with_playwright(self, page, url):
        try:
            page.goto(url)
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
        tabs = page.query_selector_all("ul.rz-tabview-nav li")
        classes = []

        for tab in tabs:
            onclick = tab.get_attribute("onclick")
            name_el = tab.query_selector("span.rz-tabview-title")

            if not onclick or not name_el:
                continue

            match = re.search(r'window.location\s*=\s*"([^"]+)"', onclick)
            if not match:
                continue

            classes.append({
                "division": name_el.inner_text().strip(),
                "url": base_domain + match.group(1)
            })

        return classes


def scrape(url, browser):
    scraper = RacingIslandsScraper()
    return scraper.run(url, browser)