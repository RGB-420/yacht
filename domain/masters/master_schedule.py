import pandas as pd

REQUIRED_COLUMNS = [""
    "regatta_name",
    "year",
    "start_date",
    "end_date"
]

def generate_master_schedule(file_path):
    df = pd.read_csv(file_path)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns in csv: {missing}")
    
    df["year"] = df["year"].astype(int)

    df["regatta_name"] = df["regatta_name"].fillna("").astype(str).str.strip()

    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")

    invalid_dates = df[
        (df["start_date"].notna()) &
        (df["end_date"].notna()) &
        (df["start_date"] > df["end_date"])
    ]

    if not invalid_dates.empty:
        print("[WARNING] Some rows have start_date > end_date")

    df = df.drop_duplicates(subset=["regatta_name", "year"])

    return df