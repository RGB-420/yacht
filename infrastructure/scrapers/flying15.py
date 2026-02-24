import pandas as pd

col_name = 4
col_number = 3
col_club = 7
col_mna = 2

def scrape(url, browser):
    df = pd.DataFrame()

    page = browser.new_page()
          
    if url:
        datos = obtener_datos(page, url)
        if datos:
                df_temp = pd.DataFrame(datos)

                df = pd.concat([df, df_temp], ignore_index=True)
        else:   
            print("No se encontraron barcos")
    else:
        print("No se pudo obtener el HTML")

    df = df.drop_duplicates()

    return df



def obtener_datos(page, url: str):
    page.goto(url)
    page.wait_for_timeout(2000)

    boats = []
    table = page.locator("div.edNews_articleContent")

    rows = table.locator("table tbody tr")
    print("Filas:", rows.count())

    for i in range(rows.count()):
        row = rows.nth(i)
        cells = row.locator("td")

        if cells.count() < 4:
            continue

        boat_name = cells.nth(col_name).inner_text().strip()
        sail_number = cells.nth(col_number).inner_text().strip()
        mna = cells.nth(col_mna).inner_text().strip()
        club = cells.nth(col_club).inner_text().strip()

        boats.append({
            "boat_name": boat_name,
            "sail_number": sail_number,
            "club": club,
            "mna":mna
        })

    return boats
