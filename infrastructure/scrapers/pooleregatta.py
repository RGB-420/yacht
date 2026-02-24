import requests
from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

df = pd.DataFrame()

col_division = 3
col_number = 6
col_boat = 4
col_class = 3
col_owner = 7
col_club = 5
col_mna = 5

nombre_csv = "Poole Regatta Handicap.csv"

def main():
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
           
    URL = "https://pooleregatta.co.uk/2022_results/Handicap_Results_2024.htm#summaryirc_national_championships_class_0"
    html = get_html_with_playwright(page, URL)
    if html:
        datos = obtener_partidos(html)
        if datos:
            guardar_datos(datos)
        else:
            print("No se encontraron partidos")
    else:
        print("No se pudo obtener el HTML")

  df.to_csv("CSV Regatas/" + nombre_csv, index=False)


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

def obtener_partidos(html):
    soup = BeautifulSoup(html, "html.parser")
    tablas= soup.find_all("table", class_="summarytable")
    print(len(tablas))
    datos = []

    for tabla in tablas:
        filas = tabla.find("tbody").find_all("tr")

        for fila in filas:
            datos_barco = fila.find_all("td")

            division = datos_barco[col_division].text
            number = datos_barco[col_number].text
            boat = datos_barco[col_boat].text
            clase = datos_barco[col_class].text
            mna = datos_barco[col_mna].text
            owner = datos_barco[col_owner].text

            datos.append([division, boat, number, clase, mna, owner])

    return datos

def guardar_datos(datos):
    global df
    df_temp = pd.DataFrame(datos, columns=["Class", "Boat", "No Sail", "Type", "mna", "Owner"])

 #   df_temp["Type"] = "Dragon"

    df = pd.concat([df, df_temp], ignore_index=True)


if __name__ == "__main__":
  main()