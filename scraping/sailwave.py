import pandas as pd
import requests
from bs4 import BeautifulSoup

df = pd.DataFrame()

#---------- CONFIGURATION ----------
# Column aliases: add new header names here if they appear in other tables
COLUMN_MAP = { 
    "division": ["Fleet"],
    "sailno": ["SailNo", "Sail Number", "Sail number", "Sail_No"],
    "boat": ["Boat", "Boat Name"],
    "type": ["Class", "Boat type"],
    "club": ["Club", "Yacht Club"],
    "owner": ["Owner", "Helm/Owner"],
    "mna": ["Boat MNA"],
}
#-----------------------------------


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

    df = df.dropna(axis=1, how="all")

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

def resolve_columns(indices, column_map):
    resolved = {}

    for logical_name, possible_headers in column_map.items():
        resolved[logical_name] = None
        for header in possible_headers:
            if header in indices:
                resolved[logical_name] = indices[header]
                break

    return resolved

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
    tablas = soup.find_all("table", class_=["summarytable", "entry"])
    print("Tablas encontradas:", len(tablas))

    datos = []

    for tabla in tablas:
        indices = get_column_indices(tabla)
        cols = resolve_columns(indices, COLUMN_MAP)

        filas = tabla.find("tbody").find_all("tr")

        for fila in filas:
            datos_barco = fila.find_all("td")

            fila_datos = {
                key: get_cell_text(datos_barco, idx)
                for key, idx in cols.items()
            }

            datos.append(fila_datos)

    return datos

