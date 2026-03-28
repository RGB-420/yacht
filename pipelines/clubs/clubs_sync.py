import pandas as pd

from app.repositories.clubs_repo import get_all_clubs_with_location

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

def sync_clubs_csv_with_db(conn, df, csv_path):
    logger.info("Starting clubs CSV sync")

    db_rows = get_all_clubs_with_location(conn)

    db_clubs = pd.DataFrame(
        db_rows,
        columns=["name", "short_name", "estimated_numbers", "city", "region", "country"]
    )

    logger.info(f"DB clubs: {len(db_clubs)} | CSV clubs: {len(df)}")

    # Comparar nombres
    csv_names = set(df["name"])
    db_names = set(db_clubs["name"])

    new_names = db_names - csv_names
    new_clubs = db_clubs[db_clubs["name"].isin(new_names)]

    if not new_clubs.empty:
        logger.info(f"{len(new_clubs)} new clubs found -> adding to CSV")

        df_updated = pd.concat([df, new_clubs], ignore_index=True)
        df_updated.to_csv(csv_path, index=False)

        logger.info(f"CSV updated: {csv_path}")

    else:
        logger.info("No new clubs found")

    logger.info("Finished clubs CSV sync")