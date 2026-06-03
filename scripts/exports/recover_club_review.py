import pandas as pd

from app.core.config import DATA_MAPPING, DATA_REVIEW

SOURCE_FILE = DATA_MAPPING / "club_mapping.csv"

REVIEW_FILE = DATA_MAPPING / "club_mapping_review.csv"

PENDING_FILE = DATA_REVIEW / "club_mapping_pending.csv"

UNRESOLVED_FILE = DATA_MAPPING / "club_mapping_unresolved.csv"

def recover_club_review():
    df = pd.read_csv(SOURCE_FILE)

    review_df = pd.DataFrame({
        "club_raw_name": df["raw_name"],
        "club_canonical_name": df["canonical_name"],
        "status": df["status"],
        "confidence": df["confidence"],
        "notes": df["notes"]
    })

    review_df = review_df.sort_values(
        by=["club_raw_name"]
    ).reset_index(drop=True)

    review_df.to_csv(REVIEW_FILE, index=False)

    print(f"Recovered {len(review_df)} rows -> {REVIEW_FILE}")

    pending_df = review_df[review_df["status"] == "pending"].copy()

    pending_df = pending_df.sort_values(by=["confidence", "club_raw_name"], ascending=[False, True], na_position="last")

    pending_df.to_csv(PENDING_FILE, index=False)

    print(f"Recovered {len(pending_df)} pending rows -> {PENDING_FILE}")

    unresolved_df = review_df[review_df["status"] == "unresolved"].copy()

    unresolved_df = unresolved_df.sort_values(by=["confidence", "club_raw_name"], ascending=[False, True], na_position="last")

    unresolved_df.to_csv(UNRESOLVED_FILE, index=False)

    print(f"Recovered {len(unresolved_df)} unresolved rows -> {UNRESOLVED_FILE}")

if __name__ == "__main__":
    recover_club_review()