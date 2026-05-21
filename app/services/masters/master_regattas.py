import pandas as pd

REQUIRED_COLUMNS = [
    "regatta_name",
    "type",
    "year",
    "status",

    "scraper_name",
    "source_type",
    "scrape_status",
    "specified_class",

    "start_date",
    "end_date",
    "notes",

    "city",
    "region",
    "country",

    "link"
]

STRING_COLUMNS = [
    "source_id",
    "regatta_name",
    "type",
    "status",

    "scraper_name",
    "source_type",
    "scrape_status",
    "specified_class",

    "notes",

    "city",
    "region",
    "country",

    "link"
]

DATE_COLUMNS = ["start_date", "end_date"]

def generate_master_regattas(file_path):
    df = pd.read_csv(file_path)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns in csv: {missing}")

    df["year"] = df["year"].astype(int)

    for col in STRING_COLUMNS:
        df[col] = df[col].fillna("").astype(str).str.strip()

    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )

    df = df.drop_duplicates()

    return df