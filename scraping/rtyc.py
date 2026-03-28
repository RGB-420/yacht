import pandas as pd
from bs4 import BeautifulSoup

COLUMN_MAP = {
    "division": "Fleet",
    "sailno": "SailNo",
    "boat": "Boat",
    "class": "Class",
    "club": "Club",
}

def scrape(url, browser):
    df = pd.DataFrame()

    page = browser.new_page()

    LINKS = get_all_links(page, url)
    
    for LINK in LINKS:
        print("Scraping: ", LINK)
        html = get_html_with_playwright(page, LINK)
        if html:
            datos = obtener_barcos(html)
            if datos:
                df_temp = pd.DataFrame(datos)

                df = pd.concat([df, df_temp], ignore_index=True)
            else:
                print("No se encontraron barcos")
        else:
            print("No se pudo obtener el HTML")

    df = df.drop_duplicates(subset=['sailno', 'boat'], keep="first")

    return df

def get_all_links(page, URL):
    html = get_html_with_playwright(page, URL)
    soup = BeautifulSoup(html, "html.parser")

    tabla = soup.find_all("table", class_="has-fixed-layout")[0]

    links = tabla.find_all("a")

    links = [a["href"] for a in tabla.find_all("a", href=True)]

    return links


def get_html_with_playwright(page, url: str) -> str:
    page.goto(url)
    page.wait_for_load_state("networkidle")
    return page.content()

def get_column_indices(tabla):
    header = tabla.find("thead").find_all("th")

    col_index = {}
    for i, th in enumerate(header):
        col_name = th.get_text(strip=True)
        col_index[col_name] = i

    return col_index

def get_cell_text(cells, idx):
    if idx is None or idx >= len(cells):
        return None
    return cells[idx].get_text(strip=True)

def obtener_barcos(html):
    soup = BeautifulSoup(html, "html.parser")
    tablas = soup.find_all("table", class_="summarytable")
    print("Tablas encontradas:", len(tablas))
    titles = soup.find_all("h3", class_="summarytitle")

    datos = []

    for i, tabla in enumerate(tablas):
        raw_table_title = titles[i].get_text(strip=True) if i < len(titles) else None

        table_title = raw_table_title.replace(" Fleet", "").strip()

        indices = get_column_indices(tabla)
        cols = {k: indices.get(v) for k, v in COLUMN_MAP.items()}

        filas = tabla.find("tbody").find_all("tr")
        print(f"Tabla {i}: filas =", len(filas), "| title =", table_title)

        for fila in filas:
            datos_barco = fila.find_all("td")

            fila_datos = {
                key: get_cell_text(datos_barco, idx)
                for key, idx in cols.items()
            }
            
            if not fila_datos.get("division"):
                fila_datos["division"] = table_title

            datos.append(fila_datos)

    return datos
