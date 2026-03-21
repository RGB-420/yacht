from pathlib import Path
import pandas as pd

from db.connection import get_engine
from db.repositories.boat_classes_repo import upsert_boat_classes

from domain.masters.master_classes import generate_master_classes

CLASSES_FILE = Path("data/classes_master.csv")

def run_classes_pipeline():
    print("Running classes pipeline...")

    if not CLASSES_FILE.exists():
        print("classes_master.csv not found")
        return
    
    df = generate_master_classes(CLASSES_FILE)

    df = df.astype(object).where(pd.notna(df), None)

    engine = get_engine()

    inserted_classes = 0

    with engine.begin() as conn:
        for _, row in df.iterrows():
            class_id, created = upsert_boat_classes(conn,
                                                    name=row['name'],
                                                    manufacturer=row['manufacturer'],
                                                    category=row['category'],
                                                    rating_rule=row['rating_rule'],
                                                    start_year=row['start_year'],
                                                    crew_min=row['crew_min'],
                                                    crew_max=row['crew_max'],
                                                    length_m=row['length_m'])
            
            if created:
                inserted_classes += 1
    
    print(f"Classes inserted: {inserted_classes}")
    print("classes pipeline finished")
    