import pandas as pd

import requests
from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse

import csv
import os
import camelot

df = pd.DataFrame()

ligas = {"competicion1": {"clase": "SB20", "link": "https://halsail-1e484.kxcdn.com/Result/Public/87777"}}

all_regatas = False
selected_regatas = ["J24 Spring Cup"]

nombre_csv = "J24 UK.csv"

def obtain_halsail():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for competicion in ligas.values():               
            URL = competicion["link"]
            if URL:
                datos = obtener_datos(page, URL)
                if datos:
                    df = guardar_datos(datos, competicion['clase'])
                else:
                    print("No se encontraron partidos")
            else:
                print("No se pudo obtener el HTML")

        df.to_csv("CSV Regatas/J24 Hailsail.csv", index=False)

def get_column_map(page, headers):
    col_map = {}
    
    for i in range(headers.count()):
        th = headers.nth(i)

        text = th.inner_text().strip()

        # botones de carreras: "Race 1", "Race 2", etc.
        if text.startswith("Race"):
            col_map[text] = i
            continue

        if text:
            col_map[text] = i

    return col_map

def get_valid_table(page):
    tables = page.locator("#divOverall table")
    count = tables.count()

    for i in range(count):
        table = tables.nth(i)

        has_thead = table.locator("thead").count() > 0
        has_tbody = table.locator("tbody").count() > 0
        rows = table.locator("tbody tr:visible")

        if has_thead and has_tbody and rows.count() > 0:
            return table

    return None

def obtener_datos(page, url: str):
    page.goto(url)
    page.wait_for_load_state("domcontentloaded")

    boats = []

    select = page.locator("#ddRacingClasses")
    options = select.locator("option:not(.text-danger)")
    print("Opciones:", options.count())

    for opt_idx in range(options.count()):
        option = options.nth(opt_idx)
        value = option.get_attribute("value")
        clase = option.inner_text().strip()

        print(f"\n➡ Seleccionando: {clase} ({value})")

        # cambia la clase
        page.select_option("#ddRacingClasses", value=value)

        # espera recarga REAL de la tabla
        page.wait_for_timeout(8000)

        table = get_valid_table(page)

        if table is None:
            print("⚠️ No se encontró tabla válida para", clase)
            continue

        headers = table.locator("thead tr th")
        rows = table.locator("tbody tr:visible")

        col_map = get_column_map(page, headers)

        for row_idx in range(rows.count()):
            row = rows.nth(row_idx)
            cells = row.locator("td")

            def safe_cell(cells, col_map, key):
                idx = col_map.get(key)
                if idx is None:
                    return None
                if idx >= cells.count():
                    return None
                return cells.nth(idx).inner_text().strip()
                    
            boats.append({
                "sail_number": safe_cell(cells, col_map, "Sail"),
                "boat_name": safe_cell(cells, col_map, "Name"),
                "type": safe_cell(cells, col_map, "Type"),
                "owner": safe_cell(cells, col_map, "Owner"),
                "club": safe_cell(cells, col_map, "Club"),
                "class": clase,
            })

    return boats

def guardar_datos(datos, clase):
    global df
    df_temp = pd.DataFrame(datos)

    #df_temp['Class'] = clase
    df_temp['Type'] = "J/24"

    df = pd.concat([df, df_temp], ignore_index=True)

    df = df.drop_duplicates()

    if all_regatas:
        return df

    else:
        df = df[df["class"].isin(selected_regatas)]

    return df

def obtener_sailwave():
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
           
    URL = "https://results.rtyc.org/regattas2025/2025RoyalTorbayRegattaJ24.htm"
    html = get_html_with_playwright(page, URL)
    if html:
        datos = obtener_partidos(html)
        if datos:
            guardar_datos_2(datos)
        else:
            print("No se encontraron partidos")
    else:
        print("No se pudo obtener el HTML")

  df.to_csv("CSV Regatas/J24 Sailwave.csv", index=False)

def get_html_with_playwright(page, url: str) -> str:
    page.goto(url)
    page.wait_for_load_state("networkidle")
    return page.content()

def obtener_partidos(html):
    soup = BeautifulSoup(html, "html.parser")
    tablas= soup.find_all("table", class_="summarytable")
    print(len(tablas))
    datos = []

    for tabla in tablas:
        filas = tabla.find("tbody").find_all("tr")

        for fila in filas:
            datos_barco = fila.find_all("td")

            division = datos_barco[1].text.strip()
            number = datos_barco[3].text.strip()
            boat = datos_barco[4].text.strip()
            club = datos_barco[9].text.strip()

            datos.append([division, boat, number, club])

    return datos

def guardar_datos_2(datos):
    global df
    df_temp = pd.DataFrame(datos, columns=["Class", "Boat", "No Sail", "Club"])

    df_temp["Type"] = "J24"

    df = pd.concat([df, df_temp], ignore_index=True)

def obtener_j24worlds():
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
           
    URL = "https://j24worlds2025.com/notice-board/results/"
    html = get_html_with_playwright(page, URL)
    if html:
        datos = obtener_partidos_2(html)
        if datos:
            guardar_datos_3(datos)
        else:
            print("No se encontraron partidos")
    else:
        print("No se pudo obtener el HTML")

  df.to_csv("CSV Regatas/J24 Worlds.csv", index=False)

def obtener_partidos_2(html):
    soup = BeautifulSoup(html, "html.parser")
    tablas= soup.find_all("table", class_="tablepress tablepress-id-2 dataTable")
    print(len(tablas))
    datos = []

    for tabla in tablas:
        filas = tabla.find("tbody").find_all("tr")

        for fila in filas:
            datos_barco = fila.find_all("td")

            number = datos_barco[3].text.strip()
            boat = datos_barco[2].text.strip()

            datos.append([boat, number])

    return datos

def guardar_datos_3(datos):
    global df
    df_temp = pd.DataFrame(datos, columns=["Boat", "No Sail"])

    df_temp["Type"] = "J24"

    df = pd.concat([df, df_temp], ignore_index=True)

def obtener_j24class():
    pdf_path = "Pdfs/J24-National.pdf"
    columns_to_keep = ["SailNo", "Boat", "Club"]

    tables = camelot.read_pdf(
            pdf_path,
            pages="1",
            flavor="stream"
        )

    if tables.n == 0:
        raise ValueError("No se encontraron tablas")

    df = tables[0].df.reset_index(drop=True)

    # 🔎 Buscar fila header real (la que contiene 'Rank')
    header_idx = None
    for i, row in df.iterrows():
        if row.astype(str).str.contains(r"\bRank\b").any():
            header_idx = i
            break

    if header_idx is None:
        raise ValueError("No se encontró la fila de encabezados")

    # 🧱 Definir columnas
    df.columns = df.iloc[header_idx].astype(str)
    df = df.iloc[header_idx + 1:].reset_index(drop=True)

    # 🧼 Limpiar nombres de columnas
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    # ❌ Eliminar columnas vacías
    if df.columns[0] == "" or df.columns[0].isspace():
        df = df.iloc[:, 1:]

    # 🔧 Si la primera columna NO se llama Rank, renombrarla
    first_col = df.columns[0]
    if first_col != "Rank":
        df = df.rename(columns={first_col: "Rank"})

    # ❌ Eliminar filas de fechas
    df = df[~df["Rank"].str.contains(r"\d{2}/\d{2}/\d{2}", na=False)]

    # ✅ Mantener solo filas válidas (1st, 2nd, 3rd...)
    df = df[df["Rank"].str.contains(r"(st|nd|rd|th)$", na=False)]

    cols = list(df.columns)

    cols[1] = "SailNo"
    cols[2] = "Boat"

    df.columns = cols

    print(df.columns.tolist())
    df[columns_to_keep].to_csv("CSV Regatas/J24 Class.csv", index=False)

def prefer_country_sail_number(series):
    """
    Prioriza sail numbers con prefijo de país (letras).
    Si no existen, devuelve el primero no vacío.
    """
    s = series.dropna().astype(str)
    s = s[s != ""]

    if s.empty:
        return None

    # 1️⃣ Primero: los que tienen letras (GBR, IRL, USA, etc.)
    with_country = s[s.str.contains(r"[A-Z]", regex=True)]
    if not with_country.empty:
        return with_country.iloc[0]

    # 2️⃣ Si no hay, devolver el primero normal
    return s.iloc[0]

def first_not_null(series):
    s = series.dropna()
    s = s[s != ""]
    return s.iloc[0] if not s.empty else None

def juntar_todo():
    column_mapping = {
        "Boat": "Name",
        "boat_name": "Name",
        "name": "Name",
        "yacht_name": "Name",
        "class": "Class", 
        "class_name": "Class",
        "Type": "Boat Type",
        "type": "Boat Type",
        "yacht_type": "Boat Type",
        "boat_type": "Boat Type",
        "handicap": "Rating",
        "rating": "Rating",
        "owner": "Owner",
        "owner_name": "Owner",
        "No Sail": "Boat Number",
        "sail_number": "Boat Number",
        "SailNo": "Boat Number",
        "yacht_club":"Club",
        "club":"Club"
    }

    csvs = ["J24 Class", "J24 Hailsail", "J24 Sailwave", "J24 Worlds"]
    dfs = []
    for csv in csvs:
        df = pd.read_csv("CSV Regatas/" + csv + ".csv")

        df = df.rename(columns=column_mapping)
    
        dfs.append(df)

    df_concat = pd.concat(dfs, ignore_index=True)

    df_concat["boat_number_norm"] = (
        df_concat["Boat Number"]
        .astype(str)
        .str.upper()
        .str.extract(r"(\d+)")
    )

    df_concat["name_norm"] = (
        df_concat["Name"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df_clean = (
        df_concat
        .groupby(["boat_number_norm", "name_norm"], as_index=False)
        .agg({
            "Boat Number": prefer_country_sail_number,
            "Name": first_not_null,
            "Club": first_not_null,
            "Class": first_not_null,
            "Boat Type": first_not_null
        })
    )
    print(df_clean.head())

    df_clean[["Boat Number", "Name", "Club", "Class", "Boat Type"]].to_csv("CSV Regatas/J24.csv", index=False)
    
if __name__ == "__main__":
    juntar_todo()