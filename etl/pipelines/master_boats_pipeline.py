from pathlib import Path
from datetime import datetime
import pandas as pd

from db.connection import get_engine
from db.repositories.raw_results_repo import get_all_raw_results

from domain.masters.master_boats import generate_master_boats

PROCESSED_DIR = Path("data/processed/masters")
BACKUP_DIR = Path("data/backups")

def backup_if_exists(path):
    if path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_&H%M%S")
        backup_path = BACKUP_DIR / f"{path.stem}_{timestamp}.csv"

    pd.read_csv(path).to_csv(backup_path, index=False)
    print(f"Backup created: {backup_path.name}")

def run_master_boats_pipeline():
    print("Running master boats pipeline...")
    engine = get_engine()

    with engine.connect() as conn:
        df_raw = get_all_raw_results(conn)

    if df_raw.empty:
        print("No raw results found in database")
        return
    
    df_boats = generate_master_boats(df_raw)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DIR / "Boats.csv"
    backup_if_exists(output_path)

    df_boats.to_csv(output_path, index=False)

    print(f"Master boats generated ({len(df_boats)} rows)")