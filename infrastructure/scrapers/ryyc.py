import pandas as pd
from bs4 import BeautifulSoup

COLUMN_MAP = {
    "sailno": "Sail No.",
    "boat": "Boat",
    "club": "Club",
    "type": "Design",
    "owner": "Person"
}

def scrape(url, browser):
    df = pd.DataFrame()

    page = browser.new_page()
    
    html = get_html_with_playwright(page, url)
    if html:
        datos = obtener_barcos(html)
        if datos:
            df_temp = pd.DataFrame(datos)

            df = pd.concat([df, df_temp], ignore_index=True)
        else:
            print("No se encontraron barcos")
    else:
        print("No se pudo obtener el HTML")

    df = df.dropna(how='all')
    df = df.drop_duplicates(subset=['sailno', 'boat'], keep="first")

    return df

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
    tablas = soup.find_all("table", class_="pretty")
    print("Tablas encontradas:", len(tablas))

    datos = []

    for i, tabla in enumerate(tablas):
        indices = get_column_indices(tabla)
        cols = {k: indices.get(v) for k, v in COLUMN_MAP.items()}

        filas = tabla.find("tbody").find_all("tr")
        print(f"Tabla {i}: filas =", len(filas))

        for fila in filas:
            datos_barco = fila.find_all("td")

            fila_datos = {
                key: get_cell_text(datos_barco, idx)
                for key, idx in cols.items()
            }

            datos.append(fila_datos)

    return datos
