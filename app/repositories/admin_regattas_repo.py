from pathlib import Path
from typing import Dict, Optional

import pandas as pd

from app.core.config import DATA_QUEUE


UNSCRAPED_PATH = DATA_QUEUE / "unscraped_regattas.csv"
SCRAPE_QUEUE_PATH = DATA_QUEUE / "scrape_queue.csv"

REGATTA_QUEUE_COLUMNS = [
    "source_id",
    "regatta_name",
    "type",
    "year",
    "status",
    "scraper_name",
    "scrape_active",
    "source_type",
    "scrape_status",
    "specified_class",
    "start_date",
    "end_date",
    "notes",
    "city",
    "region",
    "country",
    "link",
]

EDITABLE_COLUMNS = {
    "link",
    "scraper_name",
    "source_type",
    "scrape_active",
    "scrape_status",
    "specified_class",
    "notes",
}

SCRAPER_OPTIONS = [
    "archive_halsail",
    "burnhamweek",
    "cape31",
    "clubspot",
    "cowesclassic",
    "cowesweek",
    "cyber_altura",
    "eaora",
    "events2",
    "falmouthclassics",
    "flying15",
    "halsail",
    "j70",
    "manage2sail",
    "myjog",
    "racing_islands",
    "racing_rules",
    "royalsolent_pdf",
    "rtyc",
    "ryyc",
    "sailevent",
    "sailracehq",
    "sailti",
    "sailwave",
    "sailwave_pdf",
    "sailworld",
    "sportspage",
    "wlyc_pdf",
    "yachtsandyachting",
    "yachtscoring",
]

SOURCE_TYPE_OPTIONS = ["Web", "PDF"]
SCRAPE_STATUS_OPTIONS = ["", "Failed", "Scrapeado"]


def _empty_dataframe():
    return pd.DataFrame(columns=REGATTA_QUEUE_COLUMNS)


def _load_unscraped_dataframe():
    if not Path(UNSCRAPED_PATH).exists():
        return _empty_dataframe()

    df = pd.read_csv(UNSCRAPED_PATH)

    for col in REGATTA_QUEUE_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    return df[REGATTA_QUEUE_COLUMNS]


def _load_scrape_queue_dataframe():
    if not Path(SCRAPE_QUEUE_PATH).exists():
        return _empty_dataframe()

    df = pd.read_csv(SCRAPE_QUEUE_PATH)

    for col in REGATTA_QUEUE_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    return df[REGATTA_QUEUE_COLUMNS]


def _records(df):
    clean_df = df.astype(object).where(pd.notna(df), None)

    return clean_df.to_dict(orient="records")


def get_unscraped_regattas(limit: int, offset: int):
    df = _load_unscraped_dataframe()
    total = len(df)
    page_df = df.iloc[offset:offset + limit]

    return {
        "data": _records(page_df),
        "total": total,
        "limit": limit,
        "offset": offset,
    }


def update_unscraped_regatta(source_id: str, updates: Dict[str, Optional[str]]):
    df = _load_unscraped_dataframe()

    if df.empty or "source_id" not in df.columns:
        return None

    source_ids = df["source_id"].astype("string")
    matches = source_ids == source_id

    if not matches.any():
        return None

    row_index = df.index[matches][0]

    for col, value in updates.items():
        if col not in EDITABLE_COLUMNS:
            continue

        df.at[row_index, col] = value

    UNSCRAPED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(UNSCRAPED_PATH, index=False)

    updated_row = df.loc[[row_index]]

    return _records(updated_row)[0]


def add_regatta_to_scrape_queue(data: Dict[str, Optional[str]]):
    df = _load_scrape_queue_dataframe()

    row = {
        "source_id": "",
        "regatta_name": data.get("regatta_name"),
        "type": data.get("type"),
        "year": data.get("year"),
        "status": data.get("status"),
        "scraper_name": data.get("scraper_name"),
        "scrape_active": data.get("scrape_active", 0),
        "source_type": data.get("source_type"),
        "scrape_status": data.get("scrape_status"),
        "specified_class": data.get("specified_class"),
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date"),
        "notes": data.get("notes"),
        "city": data.get("city"),
        "region": data.get("region"),
        "country": data.get("country"),
        "link": data.get("link"),
    }

    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    SCRAPE_QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(SCRAPE_QUEUE_PATH, index=False)

    return row


def get_regatta_admin_options():
    return {
        "scrapers": SCRAPER_OPTIONS,
        "source_types": SOURCE_TYPE_OPTIONS,
        "scrape_statuses": SCRAPE_STATUS_OPTIONS,
    }
