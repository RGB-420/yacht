import pandas as pd

from app.core.config import DATA_MAPPING, DATA_REVIEW

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

REVIEW_PATH = DATA_MAPPING / "club_mapping_review.csv"

PENDING_PATH = DATA_REVIEW / "club_mapping_pending.csv"

UNRESOLVED_PATH = DATA_MAPPING / "club_mapping_unresolved.csv"

def sync_review_files(working_path):
    logger.info(f"Syncing working file: {working_path.name}")

    review_df = pd.read_csv(REVIEW_PATH)
    working_df = pd.read_csv(working_path)

    review_df = clean_df(review_df)
    working_df = clean_df(working_df)

    review_index = {
        row["club_raw_name"]: idx
        for idx, row in review_df.iterrows()
    }

    updated = 0
    inserted = 0

    for row in working_df.itertuples(index=False):
        raw_name = row.club_raw_name

        if pd.isna(raw_name):
            continue

        row_dict = row._asdict()

        if raw_name in review_index:
            idx = review_index[raw_name]

            for col, value in row_dict.items():
                if pd.notna(value):
                    review_df.at[idx, col] = value

            updated += 1
        
        else:
            review_df = pd.concat(
                [
                    review_df,
                    pd.DataFrame([row_dict])
                ],
                ignore_index=True
            )

            inserted += 1

    review_df = review_df.sort_values(
        by=["club_raw_name"]
    ).reset_index(drop=True)

    review_df.to_csv(REVIEW_PATH, index=False)

    logger.info(f"Rows updated: {updated}")
    logger.info(f"Rows inserted: {inserted}")

def sync_pending_to_review():
    sync_review_files(PENDING_PATH)

def sync_unresolved_to_review():
    sync_review_files(UNRESOLVED_PATH)

def clean_df(df):
    for col in df.columns:
        df[col] = df[col].astype("string").str.strip()
    
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    return df