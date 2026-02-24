from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse

import csv
import os

CSV_FILE = "CSV Regatas/Round the Island.csv"

file_exists = os.path.isfile(CSV_FILE)

FIELDNAMES = [
    "division",
    "class_name",
    "boat_name",
    "sail_number",
    "club",
    "owner",
    "boat_type",
]

CLASSES = [
    {
        "division": "IRC",
        "class_name": "IRC 0",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=0eb3eba3-d729-43a4-9642-6baa58844064&classId=&t=0&pageSize=100&pageIndex=0&method=PageChanged&class=41d016ff-74dc-4477-a0ab-98f69863d756",
        "pages": 1,
    },
        {
        "division": "IRC",
        "class_name": "IRC 1",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=0eb3eba3-d729-43a4-9642-6baa58844064&classId=&t=0&pageSize=100&pageIndex=0&method=PageChanged&class=8567bc1c-eefc-4a66-afc2-c500a399e88d",
        "pages": 1,
    },
        {
        "division": "IRC",
        "class_name": "IRC 2",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=0eb3eba3-d729-43a4-9642-6baa58844064&classId=&t=0&pageSize=100&pageIndex=0&method=PageChanged&class=83138e4e-484f-47de-8bfe-abc4ea48ae9e",
        "pages": 1,
    },
        {
        "division": "IRC",
        "class_name": "IRC 3",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=0eb3eba3-d729-43a4-9642-6baa58844064&classId=&t=0&pageSize=100&pageIndex=0&method=PageChanged&class=dc732c84-9332-489b-ac5b-a98177934a06",
        "pages": 1,
    },
        {
        "division": "IRC",
        "class_name": "Double Handed",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=0eb3eba3-d729-43a4-9642-6baa58844064&classId=&t=0&pageSize=100&pageIndex=0&method=PageChanged&class=05d52acf-63b3-4869-a160-3a258ec88d51",
        "pages": 1,
    },
        {
        "division": "ISC",
        "class_name": "ISC 4",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=3b2b2b9e-4b4d-4550-9b21-4ec5f40017e2&classId=&t=1&class=ff54f31c-3da3-4d6a-9658-c7880b1f22ba&pageIndex=0&pageSize=50",
        "pages": 2,
    },
            {
        "division": "ISC",
        "class_name": "ISC 5",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=3b2b2b9e-4b4d-4550-9b21-4ec5f40017e2&classId=&t=1&class=ed65a1c2-19b4-457d-b01a-9edfdd2826f8&pageIndex=0&pageSize=50",
        "pages": 2,
    },
            {
        "division": "ISC",
        "class_name": "ISC 6",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=3b2b2b9e-4b4d-4550-9b21-4ec5f40017e2&classId=&t=1&class=ffa9c699-8b2a-4d04-8066-2a221ccb5280&pageIndex=0&pageSize=50",
        "pages": 2,
    },
            {
        "division": "ISC",
        "class_name": "ISC 7",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=3b2b2b9e-4b4d-4550-9b21-4ec5f40017e2&classId=&t=1&class=505b038e-bf30-4123-895e-bc42f2d9b99e&pageIndex=0&pageSize=50",
        "pages": 2,
    },
            {
        "division": "ISC",
        "class_name": "ISC 8",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=3b2b2b9e-4b4d-4550-9b21-4ec5f40017e2&classId=&t=1&class=41522497-7cfc-48a4-a193-bfeae5d56b08&pageIndex=0&pageSize=50",
        "pages": 2,
    },
                {
        "division": "Clipper Yachts",
        "class_name": "Clipper Yachts",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=725bb07a-c8ba-444d-9871-3d4363fabdf5&classId=&t=2",
        "pages": 1,
    },
                    {
        "division": "Grand Prix and MOCRA Racing",
        "class_name": "Grand Prix and MOCRA 1",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=7998bf1e-27f5-45c3-9dbc-7934e5b30f80&classId=&t=3&class=3bb38421-068a-4e18-ae87-b6d2df8fefb4&pageIndex=0",
        "pages": 1,
    },
                    {
        "division": "Grand Prix and MOCRA Racing",
        "class_name": "Grand Prix and MOCRA 2",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=7998bf1e-27f5-45c3-9dbc-7934e5b30f80&classId=&t=3&class=dfa7e853-3cad-41d0-b58d-09eeae926b86&pageIndex=0",
        "pages": 1,
    },
                    {
        "division": "Multihull Bridgedeck Catamaran Cruiser",
        "class_name": "Bridgedeck Catamaran Cruiser 1",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=a8fcef36-ae62-4fe8-b807-9cbe05a862ba&classId=&t=4&class=1d189aa6-8faf-4405-b541-8c799a4cf8ce&pageIndex=0",
        "pages": 1,
    },
         {
        "division": "Gaffers",
        "class_name": "Gaffers 1",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=210e9e08-f099-437f-9742-512a7217d831&classId=&t=5&class=eaf79ac5-dbbb-49e2-a656-fab8f40cc1b7&pageIndex=0",
        "pages": 1,
    },
    {
        "division": "Gaffers",
        "class_name": "Gaffers 3",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=210e9e08-f099-437f-9742-512a7217d831&classId=&t=5&class=c40922fd-959a-428f-8f9f-226b3c96e1e4&pageIndex=0",
        "pages": 1,
    },
                    {
        "division": "Sportsboat",
        "class_name": "Sportsboat",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=2bc901c8-3fca-4f07-9d30-c78e8f897a7e&classId=&t=6",
        "pages": 1,
    },
                        {
        "division": "J/70",
        "class_name": "J/70",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=2bb021ca-6355-4305-9913-34262f72d09e&classId=&t=7",
        "pages": 1,
    },
                        {
        "division": "Sunsail 41",
        "class_name": "Sunsail 41",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=d12c34e7-ec74-4974-a8cc-6321d5d654db&classId=&t=8",
        "pages": 1,
    },
                            {
        "division": "Classic Racing Yacht",
        "class_name": "Classic Racing Yacht Over 9.6m",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=1d717772-d1f0-46f5-be83-d495cb223e6c&classId=&t=9&class=a3c14daf-c983-41f2-9cdc-c3ebcb992340&pageIndex=0",
        "pages": 1,
    },
                                {
        "division": "Classic Racing Yacht",
        "class_name": "Classic Racing Yacht Under 9.6m",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=1d717772-d1f0-46f5-be83-d495cb223e6c&classId=&t=9&class=08c3b272-0dce-423b-9964-d722f0fc94d4&pageIndex=0",
        "pages": 1,
    },                                {
        "division": "Modern Classic Racing Yachts",
        "class_name": "Modern Classic Racing Yachts",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=b7cf6c62-042f-45eb-9e77-38c5a5bb815e&classId=&t=10",
        "pages": 1,
    },                             {
        "division": "Nordic Folkboat",
        "class_name": "Nordic Folkboat",
        "url": "https://racing.islandsc.org.uk/raceresults/da6b657c-a114-4575-971f-b84e0800a22e?returnUrl=&divisionId=107ecc26-76c3-4a76-870f-7e1734cd2799&classId=&t=11",
        "pages": 1,
    },
]


def set_page_index(url, page_index):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)

    qs["pageIndex"] = [str(page_index)]
    qs["method"] = ["PageChanged"]

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

    # -------------------------
    # Boat name
    # -------------------------
    name_tag = ul.select_one("a.btn-view-boat")
    data["boat_name"] = name_tag.get_text(strip=True) if name_tag else None
    data["boat_link"] = name_tag.get("href") if name_tag else None

    # -------------------------
    # Class / sail number (MON52)
    # -------------------------
    class_tag = ul.select_one("span[style*='font-size']")
    data["sail_number"] = class_tag.get_text(strip=True) if class_tag else None


    # -------------------------
    # Collapsed section (details)
    # -------------------------
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
    print(f"      🔎 Club en {boat_url}")

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
            print(club)

    except Exception as e:
        print(f"      ⚠️ Error sacando club: {e}")
        boat_data["club"] = None

    return boat_data



def get_html_with_playwright(page, url: str) -> str:
    page.goto(url)
    page.wait_for_load_state("networkidle")
    return page.content()

with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    if not file_exists:
        writer.writeheader()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    for target in CLASSES:
        division = target["division"]
        class_name = target["class_name"]
        base_url = target["url"]
        total_pages = target["pages"]

        print(f"\n📂 División: {division}")
        print(f"🏷️ Clase: {class_name}")
        print(f"📄 Páginas: {total_pages}")

        for page_index in range(total_pages):
            page_url = set_page_index(base_url, page_index)
            print(f"  → Página {page_index + 1}")

            try:
                print(page_url)
                html = get_html_with_playwright(page, page_url)
                soup = BeautifulSoup(html, "html.parser")

                accordion = soup.find("div", id="accordion")
                if not accordion:
                    print("    ⚠️ No accordion")
                    continue

                barcos = accordion.find_all("ul", class_="rz-datalist-data")
                print(f"    ⛵ Barcos encontrados: {len(barcos)}")

                with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)

                    for ul in barcos:
                        boat_data = extract_boat_data(ul)
                        boat_data["division"] = division
                        boat_data["class_name"] = class_name
                        boat_data = extract_club(boat_data, page)
                        boat_data.pop("boat_link", None)
                        boat_data.pop("boat_url", None)
                        writer.writerow(boat_data)

            except Exception as e:
                print(f"    ❌ Error en página {page_index + 1}: {e}")

    browser.close()