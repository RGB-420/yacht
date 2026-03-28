import pandas as pd
import os
from datetime import datetime, timedelta
from pathlib import Path

from db.connection import get_engine
from db.repositories.boats_repo import get_boats_scorecard
from db.repositories.clubs_repo import get_clubs_scorecard
from db.repositories.owners_repo import get_owners_scorecard
from db.repositories.regattas_repo import get_regattas_scorecard

BASE_PATH = Path("data")

prenorm_path = BASE_PATH / "prenormalization"
mapping_path = BASE_PATH / "mapping"
scorecards_path = BASE_PATH / "scorecards"

today = datetime.now().strftime("%Y-%m-%d")

txt_path = scorecards_path / f"scorecard_weekly_{today}.txt"
csv_path = scorecards_path / f"scorecard_weekly_{today}.csv"

ENTITIES = ['boat', 'club', 'owner', 'regatta']

REPO_FUNCTIONS = {
    "boat": get_boats_scorecard,
    "club": get_clubs_scorecard,
    "owner": get_owners_scorecard,
    "regatta": get_regattas_scorecard
}

def main():
    # CSVs
    prenorm_counts = load_counts_from_folder(prenorm_path)
    mapping_counts = load_counts_from_folder(mapping_path)

    # DB
    engine = get_engine()
    week_ago = datetime.now() - timedelta(days=7)

    with engine.begin() as conn:
        db_results = get_db_metrics(conn, REPO_FUNCTIONS, ENTITIES, week_ago)

    scorecards_path.mkdir(parents=True, exist_ok=True)

    # Scorecard
    scorecard = build_scorecard(db_results, prenorm_counts, mapping_counts)

    # Export
    export_scorecard(scorecard, csv_path, txt_path)

def load_counts_from_folder(folder_path):
    counts = {}
    
    for file in folder_path.glob("*.csv"):
        entity = file.name.split("_")[0]
        df = pd.read_csv(file)
        counts[entity] = len(df)
    
    return counts

def get_db_metrics(conn, repo_functions, entities, week_ago):
    results = []

    for entity in entities:
        metrics = repo_functions[entity](conn, week_ago)

        total_active = metrics["total_active"]
        new_sourced = metrics["new_sourced"]

        results.append({
            "Entity": entity,
            "Total Active": total_active,
            "New Sourced": new_sourced
        })

    return results

def build_scorecard(db_results, prenorm_counts, mapping_counts):
    results = []

    for row in db_results:
        entity = row["Entity"]

        in_review = prenorm_counts.get(entity, 0)
        confirmed = mapping_counts.get(entity, 0)

        if entity == "regatta":
            in_review = None
            confirmed = None

        results.append({
            **row,
            "In Review": in_review,
            "Confirmed": confirmed
        })

    df = pd.DataFrame(results)

    df = df.fillna("-")
    df = df[["Entity", "Total Active", "New Sourced", "In Review", "Confirmed"]]

    for col in ["Total Active", "New Sourced", "In Review", "Confirmed"]:
        df[col] = df[col].apply(
            lambda x: int(x) if isinstance(x, float) and x != "-" else x
        )

    return df

def export_scorecard(scorecard, csv_path, txt_path):
    scorecard.to_csv(csv_path, index=False)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("WEEKLY DATA SCORECARD\n")
        f.write(f"Date: {datetime.today().date()}\n\n")

        f.write("Definitions:\n")
        f.write("- Total Active: total number of active records in the database\n")
        f.write("- New Sourced: records created in the last 7 days\n")
        f.write("- In Review: records in prenormalization (pending mapping)\n")
        f.write("- Confirmed: records already mapped and integrated\n\n")

        f.write("Note:\n")
        f.write("In Review may be higher than Total Active because multiple raw inputs can correspond to a single entity.\n\n")

        f.write("Summary:\n")
        f.write(f"- Total active records: {safe_sum(scorecard['Total Active'])}\n")
        f.write(f"- Total in review: {scorecard['In Review'].replace('-', 0).sum()}\n")
        f.write(f"- Total confirmed: {scorecard['Confirmed'].replace('-', 0).sum()}\n\n")

        f.write("Scorecard:\n\n")
        f.write(scorecard.to_string(index=False, col_space=14))

def safe_sum(series):
    return pd.to_numeric(series, errors="coerce").fillna(0).sum()

if __name__ == "__main__":
    main()   
