import pandas as pd

from playwright.sync_api import sync_playwright
from pathlib import Path

from db.connection import get_engine
from db.repositories.raw_results_repo import insert_raw_result

from infrastructure.scrapers import events2, burnhamweek, cape31, cowesclassic, flying15, j70, halsail, sailracehq, sailwave, yacthscoring, racing_islands, rtyc, sailevent, sailworld, yachtsandyachting, racing_rules, cowesweek
from infrastructure.scrapers import sailwave_pdf, royalsolent_pdf, wlyc_pdf

BASE_OUTPUT = Path("data/raw/regattas")
CONFIG_FILE = Path("infrastructure/config/ToScrape.xlsx")

SCRAPERS = {
    "events2": events2.scrape,
    "burnhamweek": burnhamweek.scrape,
    "cape31": cape31.scrape,
    "cowesclassic": cowesclassic.scrape,
    "flying15": flying15.scrape,
    "j70": j70.scrape,
    "halsail": halsail.scrape,
    "sailracehq": sailracehq.scrape,
    "sailwave": sailwave.scrape,
    "yacthscoring": yacthscoring.scrape,
    "racing_islands": racing_islands.scrape,
    "rtyc": rtyc.scrape,
    "sailevent": sailevent.scrape,
    "sailworld": sailworld.scrape,
    "yachtsandyachting": yachtsandyachting.scrape,
    "racing_rules": racing_rules.scrape,
    "cowesweek": cowesweek.scrape,

    "sailwave_pdf": sailwave_pdf.scrape,
    "royalsolent_pdf": royalsolent_pdf.scrape,
    "wlyc_pdf": wlyc_pdf.scrape
}

def run_scraper(scrape_fn, source, year, name, class_=None, source_page=None, source_type=None, browser=None):
    if browser:
        df = scrape_fn(source, browser)
    else:
        df = scrape_fn(source)

    if class_ and class_ != "No":
        df["class"] = class_

    df = df.dropna(axis=1, how="all")

    engine = get_engine()

    with engine.begin() as conn:
        print(f"Inserting raw results: {name} {year}")
        insert_raw_result(conn, source_type=source_type, source_page=source_page, regatta_name=name, year=year, data = df.to_dict(orient="records"))

    BASE_OUTPUT.mkdir(parents=True, exist_ok=True)

    df.to_csv(BASE_OUTPUT / f"{name}-{year}.csv", index=False)

def scrape_web():
    df_links = pd.read_excel(CONFIG_FILE, sheet_name="Web")
    df_links = df_links[df_links["Active"] == 1]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        for _, row in df_links.iterrows():
            pagina = row["Page"]
            if pagina not in SCRAPERS:
                print(f"⚠️  No hay scraper para {pagina}")
                continue
            try:
                run_scraper(
                    SCRAPERS[pagina],
                    row["URL"],
                    row["Year"],
                    row["Regatta Name"],
                    row["Specified Class"],
                    pagina,
                    "Web",
                    browser=browser
                )
                log_success(pagina, row["Regatta Name"])
            except Exception as e:
                log_error(pagina, row["URL"], e)

def scrape_pdfs():
    df_pdf = pd.read_excel(CONFIG_FILE, sheet_name="PDF")
    
    for _, row in df_pdf.iterrows():
        pagina = row["Page"]
        if pagina not in SCRAPERS:
            print(f"⚠️  No hay scraper para {pagina}")
            continue

        try:
            run_scraper(
                SCRAPERS[pagina],
                row["PDF Route"],
                row["Year"],
                row["Regatta Name"],
                row["Specified Class"],
                pagina,
                "PDF"
            )
            log_success(pagina, row["Regatta Name"])
        except Exception as e:
            log_error(pagina, row["PDF Route"], e)

def log_success(pagina, name):
    print(f"✅ {pagina} | {name} OK")

def log_error(pagina, source, e):
    print(f"❌ Error en {pagina} | {source}")
    print(e)
