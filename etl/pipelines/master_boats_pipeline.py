from pathlib import Path
from datetime import datetime
import pandas as pd

from domain.masters.master_boats import generate_master_boats

RAW_DIR = Path("data/raw/regattas")
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
    file_paths = list(RAW_DIR.glob("*.csv"))

    if not file_paths:
        print("No raw regatta files found")
        return
    
    df_boats = generate_master_boats(file_paths)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DIR / "Boats.csv"
    backup_if_exists(output_path)

    df_boats.to_csv(output_path, index=False)

    print(f"Master boats generated ({len(df_boats)} rows)")