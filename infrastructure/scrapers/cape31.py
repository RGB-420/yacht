import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def scrape(url, browser):
    df = pd.DataFrame()
    page = browser.new_page()
             
    if url:
        datos = obtener_datos(page, url)
        if datos:
                df_temp = pd.DataFrame(datos)
                df = pd.concat([df, df_temp], ignore_index=True)

        else:
            print("No se encontraron partidos")
    else:
        print("No se pudo obtener el HTML")

    df = df.drop_duplicates()
    return df

def set_page_index(url, page):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    qs["page"] = [str(page)]
    new_query = urlencode(qs, doseq=True)
    return urlunparse(parsed._replace(query=new_query))

def get_page_indices(html):
    soup = BeautifulSoup(html, "html.parser")

    pagination = soup.find("ul", class_="pagination")
    if not pagination:
        return [1]  # solo una página

    indices = set()

    for a in pagination.find_all("a", href=True):
        parsed = urlparse(a["href"])
        qs = parse_qs(parsed.query)

        if "page" in qs:
            try:
                indices.add(int(qs["page"][0]))
            except ValueError:
                pass

    return sorted(indices) if indices else [1]

def get_html_with_playwright(page, url: str) -> str:
    page.goto(url)
    page.wait_for_load_state("networkidle")
    return page.content()


def obtener_datos(page, url: str):
    page.goto(url)
    page.wait_for_timeout(2000)
    html = get_html_with_playwright(page, url)

    page_indices = get_page_indices(html)
    boats = []
    print(page_indices)

    for page_index in page_indices:
        page.goto(set_page_index(url, page_index))

        table = page.locator("table")
        print(page.locator("table").count())

        rows = table.locator("tbody tr")
        print("Filas:", rows.count())

        for i in range(rows.count()):
            row = rows.nth(i)
            cells = row.locator("td")

            if cells.count() < 4:
                continue

            boat_name = cells.nth(1).inner_text().strip()
            sail_number = cells.nth(2).inner_text().strip()
            owner = cells.nth(3).inner_text().strip()

            boats.append({
                "boat_name": boat_name,
                "sail_number": sail_number,
                "owner": owner
            })

    return boats

