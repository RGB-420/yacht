import pandas as pd
from pathlib import Path

OLD_FILE = Path("data/mapping/club_mapping_review_old.csv")
PENDING_FILE = Path("data/review/club_mapping_pending.csv")
TEST_FILE = Path("data/review/club_mapping_pending_test.csv")

def main():
    pending_df = pd.read_csv(PENDING_FILE)

    old_df = pd.read_csv(OLD_FILE)

    old_df = old_df[["club_raw_name", "club_canonical_name", "status", "confidence", "notes"]]

    merged_df = pending_df.merge(old_df, on="club_raw_name", how="left", suffixes=("", "_old"))

    merged_df["club_canonical_name"] = merged_df["club_canonical_name_old"].combine_first(merged_df["club_canonical_name"])

    merged_df["status"] = merged_df["status_old"].combine_first(merged_df["status"])

    merged_df["confidence"] = merged_df["confidence_old"].combine_first(merged_df["confidence"])

    merged_df["notes"] = merged_df["notes_old"].combine_first(merged_df["notes"])

    merged_df = merged_df.drop(columns=[col for col in merged_df.columns if col.endswith("_old")], errors="ignore")

    merged_df.to_csv(PENDING_FILE, index=False)

    print(f"Rows: {len(merged_df)}")

    recovered = merged_df["club_canonical_name"].notna().sum()

    print(f"Recovered mappings: {recovered}")

    pending = merged_df["status"].fillna("pending").eq("pending").sum()

    print(f"Still pending: {pending}")

    print(f"Updated -> {PENDING_FILE}")

if __name__ == "__main__":
    main()