import pandas as pd

df = pd.DataFrame()

#---------- CONFIGURATION ----------
all_regatas = True #Activate if want all regattas that appear in the left selector of the link
selected_regatas = [] #If all_regattas is false put all that you want
#-----------------------------------


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

    if all_regatas:
        return df

    else:
        df = df[df["class"].isin(selected_regatas)]

    return df


def get_column_map(page, headers):
    col_map = {}
    
    for i in range(headers.count()):
        th = headers.nth(i)

        text = th.inner_text().strip()

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


def obtener_datos(page, url):
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

