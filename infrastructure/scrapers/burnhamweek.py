from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

def scrape(url, browser):
    df = pd.DataFrame()

    page = browser.new_page()

    html = get_html_with_playwright(page, url)
    df_links = obtener_links(html)
    print(df_links.head(50))
    for row in df_links.itertuples(index=False):
        print(row.url)
        html = get_html_with_playwright(page, row.url)

        if html:
            datos = obtener_partidos(html, row.text)
            if datos:
                df_temp = pd.DataFrame(datos)
                df = pd.concat([df, df_temp], ignore_index=True)
            else:
                print("No se encontraron barcos")
        else:
            print("No se pudo obtener el HTML")
            
    df = df.drop_duplicates()
    return df


def get_html_with_playwright(page, url: str) -> str:
    page.goto(url)
    page.wait_for_load_state("networkidle")
    return page.content()

def obtener_links(html, base_url=None):
    soup = BeautifulSoup(html, "html.parser")

    data = []

    for seccion in soup.find_all("section", class_="fc_accordion"):
        for a in seccion.find_all("a", href=True):
            data.append({
                "url": urljoin(base_url, a["href"]) if base_url else a["href"],
                "text": a.get_text(strip=True)
            })

    return pd.DataFrame(data)

def get_value(celdas, col, key):
    idx = col.get(key)
    if idx is None or idx >= len(celdas):
        return None
    return celdas[idx].get_text(strip=True)

def normalizar_columnas(tabla):
    col = {}
    ths = tabla.find("thead").find_all("th")

    for i, th in enumerate(ths):
        name = th.get_text(strip=True)
        name = name.replace("\xa0", "")
        name = name.lower()
        col[name] = i

    return col

def obtener_partidos(html, clase):
    soup = BeautifulSoup(html, "html.parser")
    tablas = soup.find_all("table", class_="summarytable")

    datos = []

    for tabla in tablas:
        col = normalizar_columnas(tabla)
        filas = tabla.find("tbody").find_all("tr")

        for fila in filas:
            celdas = fila.find_all("td")

            fila_data = {
                "boat": get_value(celdas, col, "boat"),
                "sailno": get_value(celdas, col, "sailno"),
                "club": get_value(celdas, col, "club"),
                "class": clase,
                "type": get_value(celdas, col, "class"),
            }

            datos.append(fila_data)

    return datos
