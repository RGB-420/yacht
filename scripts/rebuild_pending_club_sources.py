from pathlib import Path
import pandas as pd

from db.connection import get_engine

from app.repositories.raw_results_repo import get_all_raw_results
from app.services.normalizers.clubs import split_club

OUTPUT_FILE = Path("data/review/pending_club_sources.csv")

CLUB_COLUMNS = ["Club", "club", "Team Name"]

def main():
    print("Loading raw regatta results...")

    engine = get_engine()

    with engine.begin() as conn:
        df = get_all_raw_results(conn)

    print(f"Rows loaded: {len(df)}")
    print(df.columns.tolist())

    club_frames = []

    for col in CLUB_COLUMNS:
        if col in df.columns:
            temp = df[[col, "Source"]].copy()

            temp = temp.rename(columns={col: "raw_name"})

            club_frames.append(temp)

    df = pd.concat(club_frames, ignore_index=True)

    df = df[df["raw_name"].notna()].copy()

    print(f"Rows with club: {len(df)}")

    df["raw_name"] = df["raw_name"].apply(split_club)

    df = df.explode("raw_name").reset_index(drop=True)

    df = df[df["raw_name"].notna()].copy()

    df["raw_name"] = (
        df["raw_name"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    df["regatta"] = df["Source"]

    result = df[["raw_name", "regatta"]].copy()

    result = result.drop_duplicates()

    result = result.groupby("raw_name", as_index=False).agg({"regatta": lambda x: " // ".join(sorted(set(x)))})

    result = result.sort_values(by="raw_name").reset_index(drop=True)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    result.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved {len(result)} clubs")
    print(f"Output: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
