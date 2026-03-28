import pandas as pd

all_regatas = True
selected_regatas = []

def scrape(url, browser):
    page = browser.new_page()
    page.goto(url)
    page.wait_for_load_state("domcontentloaded")

    datos = obtener_datos(page, url)

    page.close()

    df = pd.DataFrame(datos)
    df = df.drop_duplicates()

    return df


def obtener_datos(page, url: str):
    page.goto(url)
    page.wait_for_load_state("domcontentloaded")

    boats = []

    tables = page.locator("table")
    num_tables = tables.count()

    print("Tablas encontradas:", num_tables)

    for table_idx in range(num_tables):
        table = tables.nth(table_idx)
        rows = table.locator("tbody tr")
        print(rows.count())
        
        for row_idx in range(rows.count())[1:]:
            row = rows.nth(row_idx)
            cells = row.locator("td")

            sail_number = cells.nth(0).inner_text().strip()
            boat_name = cells.nth(1).inner_text().strip()

            if not sail_number:
                break

            print(sail_number)

            boats.append({
                "sail_number": sail_number,
                "boat_name": boat_name,
            })

    return boats


