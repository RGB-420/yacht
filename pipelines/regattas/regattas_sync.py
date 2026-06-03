import pandas as pd

from app.repositories.regattas_repo import get_all_regattas_master_data

from app.repositories.raw_results_repo import get_raw_regatta_sources

from pipelines.operations.sync_scrape_queue import generate_source_id

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

def sync_regattas_csv_with_db(conn, df, csv_path):
    logger.info("Starting regattas CSV sync")

    db_rows = get_all_regattas_master_data(conn)

    db_regattas = pd.DataFrame(db_rows,columns=["regatta_name", "type", "year", "status", "link", "start_date", "end_date", "city", "region", "country"])

    db_regattas["source_id"] = ""
    db_regattas["scraper_name"] = ""
    db_regattas["scrape_active"] = 0
    db_regattas["source_type"] = ""
    db_regattas["scrape_status"] = ""
    db_regattas["specified_class"] = ""
    db_regattas["notes"] = ""

    raw_rows = get_raw_regatta_sources(conn)

    raw_lookup = {}

    for regatta_name, year, source_type, source_page in raw_rows:
        key = (regatta_name, year)

        if key not in raw_lookup:
            raw_lookup[key] = {
                "source_type": source_type,
                "source_page": source_page
            }

    for idx, row in db_regattas.iterrows():
        key = (row["regatta_name"], row["year"])

        if key in raw_lookup:
            db_regattas.loc[idx, "scraper_name"] = raw_lookup[key]["source_page"]
            db_regattas.loc[idx, "source_type"] = raw_lookup[key]["source_type"]
            db_regattas.loc[idx, "scrape_status"] = "Scrapeado"

    for (regatta_name, year), group in db_regattas.groupby(["regatta_name", "year"]):
        for counter, idx in enumerate(group.index, start=1):
            db_regattas.loc[idx, "source_id"] = generate_source_id(regatta_name, year, counter)
    
    db_regattas = db_regattas[["source_id", "regatta_name", "type", "year", "status", "scraper_name", "scrape_active", "source_type", "scrape_status", "specified_class", "start_date", "end_date", "notes", "city", "region", "country", "link"]]

    if not csv_path.exists():
        logger.info(f"{csv_path} not found -> creating from DB")

        db_regattas.to_csv(csv_path, index=False)

        logger.info(f"CSV created: {csv_path}")

        return
    
    logger.info(f"DB regattas: {len(db_regattas)} | CSV regattas: {len(df)}")

    csv_keys = set(zip(df["regatta_name"], df["year"]))

    db_keys = set(zip(db_regattas["regatta_name"], db_regattas["year"]))

    new_keys = db_keys - csv_keys

    new_regattas = db_regattas[db_regattas.apply(
                    lambda row: (row["regatta_name"], row["year"]) in new_keys,
                    axis=1
    )]

    if not new_regattas.empty:
        logger.info(f"{len(new_regattas)} new regattas found")

        df_updated = pd.concat([df, new_regattas], ignore_index=True)

        df_updated.to_csv(csv_path, index=False)

        logger.info(f"CSV updated: {csv_path}")

    else:
        logger.info("No new regattas found")
    
    logger.info("Finished regattas CSV sync")