import pandas as pd

REQUIRED_COLUMNS = [
    "regatta_name",
    "type",
    "year",
    "link",
    "status",
    "city",
    "region",
    "country"
]

def generate_master_regattas(file_path):
    df = pd.read_csv(file_path)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns in csv: {missing}")

    df["year"] = df["year"].astype(int)

    for col in ["regatta_name", "type", "link", "city", "region", "country"]:
        df[col] = df[col].fillna("").astype(str).str.strip()

    df = df.drop_duplicates()

    return df