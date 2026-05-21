import pandas as pd

from playwright.sync_api import sync_playwright
from pathlib import Path

from db.connection import get_engine
from app.repositories.raw_results_repo import insert_raw_result

from scraping.webs import archive_halsail, burnhamweek, cape31, clubspot, cowesclassic, cowesweek, events2, falmouthclassics, flying15, halsail, j70, manage2sail, racing_islands, racing_rules, rtyc, ryyc, sailevent, sailracehq, myjog, eaora, sailwave, sailworld, yachtsandyachting, yachtscoring, sailti, sportspage
from scraping.pdfs import royalsolent_pdf, sailwave_pdf, wlyc_pdf

from app.core.config import DATA_RAW, DATA_MASTER

from pipelines.operations.update_scrape_status import update_scrape_status

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

BASE_OUTPUT = DATA_RAW / "regattas"
REGATTAS_MASTER_PATH = (DATA_MASTER / "regattas_master.csv")

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
    "myjog": myjog.scrape,
    "eaora": eaora.scrape,

    "sailwave_pdf": sailwave_pdf.scrape,
    "royalsolent_pdf": royalsolent_pdf.scrape,
    "wlyc_pdf": wlyc_pdf.scrape
}

def load_scrape_config():
    logger.info("Loading scrape config")

    df = pd.read_csv(REGATTAS_MASTER_PATH)

    for col in df.columns:
        df[col] = (df[col].astype("string").str.strip())
    
    df["scrape_active"] = pd.to_numeric(df["scrape_active"], errors="coerce").fillna(0).astype(int)

    df = df[df["scrape_active"] == 1].copy()

    logger.info(f"Active scrape rows: {len(df)}")

    return df

def run_scraper(scrape_fn, source, year, name, source_id, class_=None, source_page=None, source_type=None, browser=None):
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

    if pd.notna(class_) and class_ != "No":
        df["class"] = class_

    df = df.dropna(axis=1, how="all")

    records = df.replace({pd.NA: None}).replace({float("nan"): None}).to_dict(orient="records")

    engine = get_engine()

    with engine.begin() as conn:
        logger.info(f"Inserting raw results: {name} {year}")
        insert_raw_result(conn, source_type=source_type, source_page=source_page, regatta_name=name, year=year, data=records)

    BASE_OUTPUT.mkdir(parents=True, exist_ok=True)

    output_path = BASE_OUTPUT / f"{name}-{year}.csv"
    df.to_csv(output_path, index=False)

    logger.info(f"Saved CSV: {output_path}")

    update_scrape_status(source_id=source_id)

def scrape_regattas():
    df = load_scrape_config()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        for _, row in df.iterrows():
            scraper_name = row["scraper_name"]

            if scraper_name not in SCRAPERS:
                logger.warning(f"No scraper found for {scraper_name}")
                continue

            source_type = str(row["source_type"]).lower()

            try:
                if source_type == "web":
                    run_scraper(
                        SCRAPERS[scraper_name],
                        row["link"],
                        row["year"],
                        row["regatta_name"],
                        row["source_id"],
                        row["specified_class"],
                        scraper_name,
                        "Web",
                        browser=browser
                    )
                
                elif source_type == "pdf":
                    run_scraper(
                        SCRAPERS[scraper_name],
                        row["link"],
                        row["year"],
                        row["regatta_name"],
                        row["source_id"],
                        row["specified_class"],
                        scraper_name,
                        "PDF",
                    )

                else:
                    logger.warning(f"Unknown source type: {source_type}")
                    continue
            
            except Exception as e:
                logger.error(f"Error in {scraper_name} | {row['link']}")

                logger.error(str(e))
