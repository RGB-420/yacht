import pandas as pd
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

def scrape(url, browser):
    page = browser.new_page()
            
    datos = obtener_datos(page, url)

    df = pd.DataFrame(datos)

    df = df.drop_duplicates()

    return df

def get_column_map(table):
    header_row = table.locator("tbody tr").first
    header_cells = header_row.locator("th")

    col_map = {}

    for i in range(header_cells.count()):
        text = header_cells.nth(i).inner_text().strip().lower()

        if "class" in text:
            col_map["Class"] = i
        elif "sailno" in text or "no" in text:
            col_map["SailNo"] = i
        elif "club" in text:
            col_map["Club"] = i

    return col_map

def accept_cookies(page, timeout=3000):
    try:
        page.locator("#ButtonEnter").wait_for(state="visible", timeout=timeout)
        page.locator("#ButtonEnter").click()
        print("Cookies aceptadas")
    except PlaywrightTimeoutError:
        pass

def obtener_datos(page, url: str):
    page.goto(url)
    page.wait_for_timeout(2000)

    accept_cookies(page)

    page.select_option(
        "#DDLEvents",
        label="Race Week 2025"
    )
    page.wait_for_load_state("networkidle")

    class_select = page.locator("select").nth(1)
    options = class_select.locator("option")
    all_rows = []

    for i in range(options.count()):
        class_value = options.nth(i).get_attribute("value")
        class_name = options.nth(i).inner_text().strip()

        if not class_name:
            continue

        print(f"Scrapeando clase: {class_name}")

        class_select.select_option(class_value)
        page.wait_for_timeout(1500)

        table = page.locator("table").nth(1)
        rows = table.locator("tbody tr")

        if rows.count() < 2:
            continue

        col_map = get_column_map(table)

        for r in range(1, rows.count()):
            row = rows.nth(r)
            cells = row.locator("td")

            if cells.count() == 0:
                continue

            sailno = (
                cells.nth(col_map["SailNo"]).inner_text().strip()
                if "SailNo" in col_map else None
            )

            club = (
                cells.nth(col_map["Club"]).inner_text().strip()
                if "Club" in col_map else None
            )

            class_value = (
                cells.nth(col_map["Class"]).inner_text().strip()
                if "Class" in col_map else class_name  # ⬅ fallback al select
            )

            if not sailno:
                continue
            
            all_rows.append({
                "Boat Number": sailno,
                "Club": club,
                "Class": class_value
            })

    return all_rows
