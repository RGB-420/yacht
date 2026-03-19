import requests
import pandas as pd
from urllib.parse import urljoin

def scrape(url, browser):
    df = pd.DataFrame()
    page = browser.new_page()
            
    links = obtener_links_resultados(page, url)
    for link in links:
        datos = obtener_datos(page, link['url'], link['title'])
        if datos:
            df_temp = pd.DataFrame(datos)

            df = pd.concat([df, df_temp], ignore_index=True)
        else:
            print("No se encontraron partidos")

    df = df.drop_duplicates()
    return df


def get_html_with_playwright(page, url: str) -> str:
    page.goto(url)
    page.wait_for_load_state("networkidle")
    return page.content()

def obtener_html(session, URL):
    try:
        response = session.get(URL, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error obteniendo {URL}: {e}")
        return None

def obtener_links_resultados(page, base_url):
    page.goto(base_url)
    page.wait_for_selector("table")

    links = []

    anchors = page.locator(
        "table.com-content-category__table tbody th.list-title a"
    )

    count = anchors.count()
    for i in range(count):
        href = anchors.nth(i).get_attribute("href")
        title = anchors.nth(i).inner_text().strip()

        if not href:
            continue

        title_clean = (
            title
            .replace("Racing Results for Cowes Classics Regatta 2025", "")
            .strip()
        )

        full_url = urljoin(base_url, href)

        links.append({
            "url": full_url,
            "title": title_clean
        })

    return links

def get_column_map(table):
    header_row = table.locator("thead tr").first
    header_cells = header_row.locator("th")

    col_map = {}

    for i in range(header_cells.count()):
        text = header_cells.nth(i).inner_text().strip().lower()
        print(text)
        if "boat" in text:
            col_map["Name"] = i
        elif "sail number" in text or "sailno" in text or "sail no." in text:
            col_map["SailNo"] = i
        elif "design" in text:
            col_map["Type"] = i

    return col_map

def obtener_datos(page, url: str, clase):
    page.goto(url)
    page.wait_for_timeout(3000)

    table = page.locator("table").first
    rows = table.locator("tbody tr")

    col_map = get_column_map(table)

    boats = []

    for r in range(rows.count()):
        row = rows.nth(r)
        cells = row.locator("td")

        if cells.count() == 0:
            continue

        sailno = (
            cells.nth(col_map["SailNo"]).inner_text().strip()
            if "SailNo" in col_map else None
        )
        
        name = (
            cells.nth(col_map["Name"]).inner_text().strip()
            if "Name" in col_map else None
        )

        type = (
            cells.nth(col_map["Type"]).inner_text().strip()
            if "Type" in col_map else None
        )

        boats.append({
            "Boat Number": sailno,
            "Name": name,
            "Class": clase,
            "Type":type
        })

    return boats
