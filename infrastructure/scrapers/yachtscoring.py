import pandas as pd

COLUMN_MAP = {
    "sailno": ["sailno", "sail number"],
    "boat": ["boat", "boat name", "yacht name"],
    "class": ["class"],
    "type": ["boat type", "yacht type"],
    "club": ["club", "yacht club"],
    "owner": ["owner", "owner's name"]
}

def scrape(url, browser):
    df = pd.DataFrame()
    page = browser.new_page()        
    if url:
        datos = obtener_datos(page, url)
        if datos:
            df_temp = pd.DataFrame(datos)

            df = pd.concat([df, df_temp], ignore_index=True)

            df = df.drop_duplicates()
            df = conseguir_owner_y_club(page, df)
        else:
            print("No se encontraron barcos")
        
    df = df.drop(columns=["boat_link", "boat_url"])
    df = df.dropna(axis=1, how="all")

    return df

def get_cell_text(cells, col_index, key):
    idx = col_index.get(key)
    if idx is None or idx >= cells.count():
        return None
    return cells.nth(idx).inner_text().strip()


def get_cell_link(cells, col_index, key):
    idx = col_index.get(key)
    if idx is None or idx >= cells.count():
        return None

    link = cells.nth(idx).locator("a")
    if link.count() == 0:
        return None

    return link.first.get_attribute("href")

def normalize(text: str) -> str:
    return (
        text.replace("\xa0", " ")
            .strip()
            .lower()
    )

def build_column_index(table):
    col_index = {}

    headers = table.locator("thead").first.locator("td")

    header_texts = []
    for i in range(headers.count()):
        header_texts.append(normalize(headers.nth(i).inner_text()))

    for standard_name, variants in COLUMN_MAP.items():
        for i, header in enumerate(header_texts):
            if header in variants:
                col_index[standard_name] = i
                break

    return col_index

def normalizar_columnas(tabla):
    col = {}
    headers = tabla.locator("thead").first.locator("td")

    for i in range(headers.count()):
        name = headers.nth(i).inner_text().strip().lower()
        col[name] = i

    return col

def obtener_datos(page, url: str):
    page.goto(url)
    page.wait_for_timeout(8000)

    boats = []

    table_container = page.locator("#main-table-container")
    table = table_container.locator("table")

    col_index = build_column_index(table)

    tbody = table.locator("tbody")
    rows = tbody.locator("tr")

    for i in range(rows.count()):
        row = rows.nth(i)
        cells = row.locator("td")

        fila_data = {
            "sailno": get_cell_text(cells, col_index, "sailno"),
            "boat": get_cell_text(cells, col_index, "boat"),
            "class": get_cell_text(cells, col_index, "class"),
            "club": get_cell_text(cells, col_index, "club"),
            "owner": get_cell_text(cells, col_index, "owner"),
            "boat_link": get_cell_link(cells, col_index, "boat"),
        }

        boats.append(fila_data)

    return boats

def conseguir_owner_y_club(page, df):
    BASE_URL = "https://yachtscoring.com"

    if "boat_url" not in df.columns:
        df["boat_url"] = BASE_URL + df["boat_link"]
        df = df.dropna(subset=["boat_url"])

    for idx, row in df.iterrows():
        boat_url = row["boat_url"]
        print(f"Scrapeando {boat_url}")

        page.goto(boat_url)
        page.wait_for_timeout(2000)

        # --- OWNER ---
        owner = None
        owner_locator = page.locator("div.font-bold", has_text="Name:")
        if owner_locator.count() > 0:
            owner = (
                owner_locator.first
                .locator("..")
                .locator("div")
                .nth(1)
                .inner_text()
                .strip()
            )

        # --- CLUB ---
        club = None
        club_locator = page.locator("div.font-bold", has_text="Yacht Club:")
        if club_locator.count() > 0:
            club = (
                club_locator.first
                .locator("..")
                .locator("div")
                .nth(1)
                .inner_text()
                .strip()
            )

        df.loc[idx, "owner"] = owner
        df.loc[idx, "club"] = club

        print(f"  Owner: {owner}")
        print(f"  Club: {club}")

    return df
