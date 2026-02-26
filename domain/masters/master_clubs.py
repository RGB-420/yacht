import pandas as pd

REQUIRED_COLUMNS = ['name', 'short_name', 'estimated_numbers', 'city', 'region', 'country']

def generate_master_clubs(file_path):
    df = pd.read_csv(file_path)

    df.columns = (df.columns.str.strip().str.lower())

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")
    
    df['name'] = df['name'].str.strip()
    df['short_name'] = df['short_name'].str.strip()

    df = df.drop_duplicates(subset=['name'])

    return df