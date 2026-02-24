import pandas as pd

def scrape(url, browser):
    page = browser.new_page()

    datos = obtener_datos(page, url)

    df = pd.DataFrame(datos)

    df = df.drop_duplicates()

    return df

def normalizar_columnas(table):
    col = {}

    header_row = table.locator("tbody tr").first
    headers = header_row.locator("th")

    for i in range(headers.count()):
        name = headers.nth(i).inner_text().strip()
        name = name.replace("\xa0", "")
        name = name.lower()
        col[name] = i

    return col

def get_value(cells, col_map, key):
    idx = col_map.get(key.lower())
    if idx is None or idx >= cells.count():
        return None
    return cells.nth(idx).inner_text().strip()

def obtener_datos(page, url: str):
    page.goto(url)
    page.wait_for_timeout(2000)

    boats = []

    table = page.locator("table.results")

    col_map = normalizar_columnas(table)

    rows = table.locator("tbody tr")
    print(rows.count())

    for i in range(rows.count()):
        row = rows.nth(i)
        if row.locator("td").count() == 0:
            continue

        cells = row.locator("td")

        data = {
            "sail_number": get_value(cells, col_map, "sail no"),
            "boat_name": get_value(cells, col_map, "boat name"),
            "owner": get_value(cells, col_map, "owner(s)"),
            "club": get_value(cells, col_map, "club")
        }

        boats.append(data)

    return boats
