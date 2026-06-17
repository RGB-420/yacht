from pathlib import Path

import pandas as pd

from db.connection import get_engine

EXPORT_DIR = Path("data/exports")

TABLES = {
    "boats": "SELECT * FROM yacht_db.boats",
    "owners": "SELECT * FROM yacht_db.owners",
    "clubs": "SELECT * FROM yacht_db.clubs",
    "clubs_normalized": "SELECT * FROM yacht_norm.clubs",
    "regattas": "SELECT * FROM yacht_db.regattas",
    "results": "SELECT * FROM yacht_raw.raw_regatta_results"
}

def export_table(engine, name: str, query: str):
    print(f"Exporting {name}...")

    df = pd.read_sql(query, engine)

    output_file = EXPORT_DIR / f"{name}.csv"

    df.to_csv(output_file, index=False)

    print(f"✓ {name}: {len(df):,} rows")

    return len(df)

def generate_summary(engine):
    queries = {
    "boats": "SELECT COUNT(*) AS total FROM yacht_db.boats",
    "owners": "SELECT COUNT(*) AS total FROM yacht_db.owners",
    "clubs": "SELECT COUNT(*) AS total FROM yacht_db.clubs",
    "regattas": "SELECT COUNT(*) AS total FROM yacht_db.regattas",
    "results": "SELECT COUNT(*) AS total FROM yacht_raw.raw_regatta_results",
    }

    summary = []

    for name, query in queries.items():
        count = pd.read_sql(query, engine).iloc[0]["total"]

        summary.append({
            "dataset": name,
            "records": count
        })

    summary_df = pd.DataFrame(summary)

    summary_df.to_csv(
        EXPORT_DIR / "dataset_summary.csv",
        index=False
    )

    return summary_df

def main():
    engine = get_engine()

    print("Exporting datasets...\n")

    for name, query in TABLES.items():
        export_table(engine, name, query)

    summary = generate_summary(engine)

    print("\nDataset Summary")
    print(summary)

if __name__ == "__main__":
    main()