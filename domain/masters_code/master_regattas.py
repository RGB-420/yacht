import pandas as pd

REQUIRED_COLUMNS = [
    "regatta_name",
    "type",
    "year",
    "link"
]

def generate_master_regattas(file_path):
    df = pd.read_csv(file_path)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns in csv: {missing}")
    
    df["regatta_name"] = df["regatta_name"].str.strip()
    df["type"] = df["type"].str.strip()

    df["year"] = df["year"].astype(int)
    df["link"] = df["link"].fillna("").astype(str).str.strip()

    df = df.drop_duplicates()

    return df