import pandas as pd

from playwright.sync_api import sync_playwright
from pathlib import Path

from db.connection import get_engine
from app.repositories.raw_results_repo import insert_raw_result


from scraping.webs import archive_halsail, burnhamweek, cape31, clubspot, cowesclassic, cowesweek, events2, falmouthclassics, flying15, halsail, j70, manage2sail, racing_islands, racing_rules, rtyc, ryyc, sailevent, sailracehq, sailwave, sailworld, yachtsandyachting, yachtscoring, sailti, sportspage
from scraping.pdfs import royalsolent_pdf, sailwave_pdf, wlyc_pdf

from app.core.config import DATA_RAW, BASE_DIR

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

BASE_OUTPUT = DATA_RAW / "regattas"
CONFIG_FILE = BASE_DIR / "infrastructure/config/ToScrape.xlsx"

SCRAPERS = {
    "events2": events2.scrape,
    "burnhamweek": burnhamweek.scrape,
    "cape31": cape31.scrape,
    "cowesclassic": cowesclassic.scrape,
    "flying15": flying15.scrape,
    "j70": j70.scrape,
    "halsail": halsail.scrape,
    "archive_halsail": archive_halsail.scrape,
    "sailracehq": sailracehq.scrape,
    "sailwave": sailwave.scrape,
    "yachtscoring": yachtscoring.scrape,
    "racing_islands": racing_islands.scrape,
    "rtyc": rtyc.scrape,
    "sailevent": sailevent.scrape,
    "sailworld": sailworld.scrape,
    "yachtsandyachting": yachtsandyachting.scrape,
    "racing_rules": racing_rules.scrape,
    "cowesweek": cowesweek.scrape,
    "falmouthclassics": falmouthclassics.scrape,
    "ryyc": ryyc.scrape,
    "clubspot": clubspot.scrape,
    "manage2sail": manage2sail.scrape,
    "sailti": sailti.scrape,
    "sportspage": sportspage.scrape,

    "sailwave_pdf": sailwave_pdf.scrape,
    "royalsolent_pdf": royalsolent_pdf.scrape,
    "wlyc_pdf": wlyc_pdf.scrape
}

def run_scraper(scrape_fn, source, year, name, class_=None, source_page=None, source_type=None, browser=None):
    logger.info(f"Scraping {source_page} | {name} ({year})")
        
    try:
        if browser:
            df = scrape_fn(source, browser)
        else:
            df = scrape_fn(source)

        logger.info(f"Rows scraped: {len(df)}")

    except Exception as e:
        logger.error(f"Scraper failed: {source_page} | {name} | {source}")
        logger.error(str(e))
        raise

    if class_ and class_ != "No":
        df["class"] = class_

    df = df.dropna(axis=1, how="all")

    engine = get_engine()

    with engine.begin() as conn:
        logger.info(f"Inserting raw results: {name} {year}")
        insert_raw_result(conn, source_type=source_type, source_page=source_page, regatta_name=name, year=year, data = df.to_dict(orient="records"))

    BASE_OUTPUT.mkdir(parents=True, exist_ok=True)

    output_path = BASE_OUTPUT / f"{name}-{year}.csv"
    df.to_csv(output_path, index=False)

    logger.info(f"Saved CSV: {output_path}")

def scrape_web():
    logger.info("Loading web scraping config")

    df_links = pd.read_excel(CONFIG_FILE, sheet_name="Web")
    df_links = df_links[df_links["Active"] == 1]

    logger.info(f"Active web scrapers: {len(df_links)}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        for _, row in df_links.iterrows():
            pagina = row["Page"]
            if pagina not in SCRAPERS:
                logger.warning(f"No scraper found for {pagina}")
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
                logger.info(f"{pagina} | {row['Regatta Name']} OK")

            except Exception as e:
                logger.error(f"Error in {pagina} | {row['URL']}")
                logger.error(str(e))

def scrape_pdfs():
    logger.info("Loading PDF scraping config")
    
    df_pdf = pd.read_excel(CONFIG_FILE, sheet_name="PDF")
    df_pdf = df_pdf[df_pdf["Active"] == 1]

    logger.info("Loading PDF scraping config")
    
    for _, row in df_pdf.iterrows():
        pagina = row["Page"]
        if pagina not in SCRAPERS:
            logger.warning(f"No scraper found for {pagina}")
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

            logger.info(f"{pagina} | {row['Regatta Name']} OK")

        except Exception as e:
            logger.error(f"Error in {pagina} | {row['PDF Route']}")
            logger.error(str(e))


