from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse
import pandas as pd

import re

BASE_DOMAIN = "https://racing.islandsc.org.uk/"

def scrape(url, browser):
    df = pd.DataFrame()

    LINKS = []
    page = browser.new_page()

    page.goto(url)

    link_type = get_link_type(url)
    print(f"\n🔗 Procesando: {url}")
    print(f"📌 Tipo: {link_type}")

    if link_type == "race_results":
        LINKS.append(url)

    elif link_type == "event_results":
        race_links = get_race_results_from_event(page)

        print(f"🏁 Carreras encontradas: {len(race_links)}")

        for r in race_links:
            print("   →", r)

        LINKS.extend(race_links)

    else:
        print("⚠️ Tipo de link desconocido, se ignora")

    for LINK in LINKS:
        page = browser.new_page()

        page.goto(LINK)

        CLASSES = get_tabs_from_tablist(page, BASE_DOMAIN)

        for target in CLASSES:
            if target["division"] == "#Tags":
                continue

            division = target["division"]
            base_url = target["url"]

            print(f"\n📂 División: {division}")

            html = get_html_with_playwright(page, base_url)
            soup = BeautifulSoup(html, "html.parser")

            subclasses = get_subclasses_from_page(soup)

            irc_overall = [s for s in subclasses if s["subclass_name"] == "IRC Overall"]
            isc_overall = [s for s in subclasses if s["subclass_name"] == "ISC Overall"]
            if irc_overall:
                subclasses = irc_overall
            if isc_overall:
                subclasses = isc_overall
            elif not subclasses:
                subclasses = [{
                    "subclass_name": None,
                    "url": base_url
                }]

            for sub in subclasses:
                subclass_name = sub["subclass_name"]
                sub_url = sub["url"]

                print(f"   🔸 Subclase: {subclass_name}")

                # 🔹 paginación POR subclase
                html = get_html_with_playwright(page, sub_url)
                soup = BeautifulSoup(html, "html.parser")
                page_indices = get_page_indices(soup)

                print(f"     📄 Páginas: {len(page_indices)}")

                for page_index in page_indices:
                    page_url = set_page_index(sub_url, page_index)
                    print(f"      → Página {page_index + 1}")

                    try:
                        html = get_html_with_playwright(page, page_url)
                        soup = BeautifulSoup(html, "html.parser")

                        accordion = soup.find("div", id="accordion")
                        if not accordion:
                            print("        ⚠️ No accordion")
                            continue

                        barcos = accordion.find_all("ul", class_="rz-datalist-data")
                        print(f"        ⛵ Barcos encontrados: {len(barcos)}")


                        for ul in barcos:
                            boat_data = extract_boat_data(ul)
                            boat_data["class_name"] = division
                            boat_data = extract_club(boat_data, page)

                            if boat_data:
                                df_temp = pd.DataFrame([boat_data])

                                df = pd.concat([df, df_temp], ignore_index=True)

                    except Exception as e:
                        print(f"        ❌ Error en página {page_index + 1}: {e}")


    df_dedup = df.drop_duplicates(
        subset=["boat_name", "sail_number"],
        keep="first"  
    )

    df_dedup = df_dedup[['boat_name', 'sail_number', 'owner', 'boat_type', 'class_name']]

    return df_dedup

def get_link_type(url: str) -> str:
    path = urlparse(url).path.lower()

    if path.startswith("/raceresults"):
        return "race_results"

    if path.startswith("/results/event"):
        return "event_results"

    return "unknown"

def get_race_results_from_event(page) -> list[str]:
    page.wait_for_load_state("networkidle")

    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    links = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/raceresults/" in href:
            full_url = urljoin("https://racing.islandsc.org.uk/", href)
            links.add(full_url)

    return sorted(links)

def set_page_index(url, page_index, page_size=25):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)

    qs["pageIndex"] = [str(page_index)]
    qs["method"] = ["PageChanged"]
    qs["pageSize"] = [str(page_size)]

    new_query = urlencode(qs, doseq=True)
    return urlunparse(parsed._replace(query=new_query))

def get_page_indices(soup):
    pagination = soup.find("ul", class_="pagination")
    if not pagination:
        return [0]  # solo una página

    indices = set()

    for a in pagination.find_all("a", href=True):
        parsed = urlparse(a["href"])
        qs = parse_qs(parsed.query)

        if "pageIndex" in qs:
            try:
                indices.add(int(qs["pageIndex"][0]))
            except ValueError:
                pass

    return sorted(indices) if indices else [0]

def extract_boat_data(ul):
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
            if not label_div:
                return None
            value_div = label_div.find_next("div", class_="small")
            return value_div.get_text(strip=True) if value_div else None

        data["owner"] = get_detail("Owner")
        data["boat_type"] = get_detail("Boat Type")
    else:
        data["owner"] = None
        data["boat_type"] = None

    return data

def extract_club(boat_data, page):
    BASE_URL = "https://racing.islandsc.org.uk/"

    if not boat_data.get("boat_link"):
        boat_data["Club"] = None
        return boat_data

    boat_url = BASE_URL + boat_data["boat_link"]

    try:
        page.goto(boat_url)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(1000)

        club_locator = page.locator("div.col-lg-4", has_text="club")

        if club_locator.count() == 0:
            boat_data["club"] = None
        else:
            club = (
                club_locator
                    .locator("..")
                    .locator("div.col.font-weight-bold")
                    .first
                    .inner_text()
                    .strip()
            )
            boat_data["club"] = club

    except Exception as e:
        print(f"      ⚠️ Error sacando club: {e}")
        boat_data["club"] = None

    return boat_data

def get_html_with_playwright(page, url: str) -> str:
    page.goto(url)
    page.wait_for_load_state("networkidle")
    return page.content()

def get_subclasses_from_page(soup):
    ul = soup.find("ul", class_="classes-wrapper")
    if not ul:
        return []

    subclasses = []

    for a in ul.find_all("a", href=True):
        name = a.get_text(strip=True)
        url = a["href"]

        subclasses.append({
            "subclass_name": name,
            "url": url
        })

    return subclasses

def get_tabs_from_tablist(page, base_domain):
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

        url = base_domain + match.group(1)
        division = name_el.inner_text().strip()

        classes.append({
            "division": division,
            "url": url
        })

    return classes

