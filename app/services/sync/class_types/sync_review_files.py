import pandas as pd

from app.core.config import DATA_MAPPING, DATA_REVIEW

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

REVIEW_PATH = DATA_MAPPING / "class_types/class_type_review.csv"

PENDING_PATH = DATA_REVIEW / "class_type_pending.csv"

UNRESOLVED_PATH = DATA_MAPPING / "class_types/class_type_unresolved.csv"

IGNORED_PATH = DATA_MAPPING / "class_types/class_type_ignored.csv"

def sync_review_files(working_path):
    logger.info(F"Syncing working file: {working_path.name}")

    review_df = pd.read_csv(REVIEW_PATH)
    working_df = pd.read_csv(working_path)

    review_df = clean_df(review_df)
    working_df = clean_df(working_df)

    review_index = {
        (row["raw_class"], row["raw_type"]): idx
        for idx, row in review_df.iterrows()
    }

    updated = 0
    inserted = 0

    for row in working_df.itertuples(index=False):
        key = (row.raw_class, row.raw_type)

        if pd.isna(row.raw_class) and pd.isna(row.raw_type):
            continue

        row_dict = row._asdict()

        if key in review_index:
            idx = review_index[key]

            for col, value in row_dict.items():
                if pd.notna(value):
                    review_df.at[idx, col] = value

            updated += 1
        
        else:
            review_df = pd.concat([review_df, pd.DataFrame([row_dict])], ignore_index=True)
            
            inserted += 1

    review_df = review_df.sort_values(by=["raw_class", "raw_type"]).reset_index(drop=True)

    review_df.to_csv(REVIEW_PATH, index=False)

    logger.info(f"Rows updated: {updated}")
    logger.info(f"Rows inserted: {inserted}")

def sync_class_type_pending_to_review():
    sync_review_files(PENDING_PATH)

def sync_class_type_unresolved_to_review():
    sync_review_files(UNRESOLVED_PATH)

def sync_class_type_ignored_to_review():
    sync_review_files(IGNORED_PATH)

def clean_df(df):
    for col in df.columns:
        df[col] = df[col].astype("string").str.strip()

    df = df.replace(r"^\s*$", pd.NA, regex=True)

    return df