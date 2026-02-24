import pandas as pd
from urllib.parse import urljoin

base_url = "https://www.cowesweek.co.uk/web/code/php/"

FIELDS = ['sail_number', 'entered_by', 'design_type']

def scrape(url, browser):
    df = pd.DataFrame()

    page = browser.new_page()

    values = get_all_select_values(page, url)

    for value in values:
        go_to_selector(page, url, value)
        print(value)

        links_barcos = obtener_links_barcos(page)
        for link in links_barcos:
            print(link)
            datos = obtener_datos_barcos(page, link)

            if datos:
                df_temp = pd.DataFrame([datos])

                df = pd.concat([df, df_temp], ignore_index=True)
            else:
                print("No se encontraron datos")

    df = df.drop_duplicates()
    df = df.rename(columns={'entered_by':'owner', 'design_type':'type'})

    return df


def get_all_select_values(page, url):
    page.goto(url)
    page.wait_for_load_state("networkidle")

    values = page.eval_on_selector_all(
        "select[name='resultrequest'] option",
        "options => options.map(o => o.value).filter(v => v !== '0')"
    )

    return values

def go_to_selector(page, url, value):
    page.goto(url)
    page.wait_for_load_state("networkidle")

    page.select_option("select[name='resultrequest']", value=value)
    page.click("button[name='submit']")

    # espera real a que aparezca la tabla
    page.wait_for_selector("div.resultspage table")

def obtener_links_barcos(page):
    rows = page.locator("div.resultspage table tr").all()

    data = []

    for row in rows[1:]:
        cells = row.locator("td")
        if cells.count() < 2:
            continue

        link = cells.nth(1).locator("a")
        if link.count() == 0:
            continue

        href = link.get_attribute("href")
        full_url = urljoin(base_url, href)

        data.append(full_url)

    return data

def obtener_datos_barcos(page, url):
    page.goto(url)

    if not page.locator("div.two-thirds").count():
        print(f"Página vacía: {url}")
        return None

    data = {}

    try:
        h3 = page.locator("div.two-thirds h3")
        data["boat_name"] = h3.evaluate(
            "el => el.childNodes[0].textContent.trim()"
        )
        data["boat_class"] = h3.locator("span").inner_text().strip()
    except Exception:
        print(f"Header incompleto: {url}")

    table = page.locator("div.two-thirds table.SearchDetails")

    if table.count():
        rows = table.locator("tbody tr")

        for i in range(rows.count()):
            row = rows.nth(i)
            cells = row.locator("td")

            if cells.count() < 2:
                continue

            key = cells.nth(0).inner_text().strip()
            value = cells.nth(1).inner_text().strip()

            key = key.lower().replace(" ", "_")

            if key in FIELDS:
                data[key] = value
    else:
        print(f"Sin tabla de detalles: {url}")

    if not data:
        return None

    return data
