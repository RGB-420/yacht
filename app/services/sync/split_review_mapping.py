import pandas as pd

from app.core.config import DATA_MAPPING

from pipelines.common.logger import get_logger

logger = get_logger(__name__)


REVIEW_PATH = DATA_MAPPING / "clubs/club_mapping_review.csv"

RESOLVED_PATH = DATA_MAPPING / "clubs/club_mapping_resolved.csv"

UNRESOLVED_PATH = DATA_MAPPING / "clubs/club_mapping_unresolved.csv"

IGNORED_PATH = DATA_MAPPING / "clubs/club_mapping_ignored.csv"

def split_review_mapping():
    logger.info("Splitting review mapping...")

    df = pd.read_csv(REVIEW_PATH)

    logger.info(f"Rows loaded: {len(df)}")

    for col in df.columns:
        df[col] = df[col].astype("string").str.strip()
    
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    resolved_df = df[df["status"] == "resolved"].copy()

    unresolved_df = df[df["status"] == "unresolved"].copy()

    ignored_df = df[df["status"] == "ignored"].copy()

    resolved_df = resolved_df.sort_values(by=["club_raw_name"]).reset_index(drop=True)

    unresolved_df = unresolved_df.sort_values(by=["club_raw_name"]).reset_index(drop=True)

    ignored_df = ignored_df.sort_values(by=["club_raw_name"]).reset_index(drop=True)

    resolved_df.to_csv(RESOLVED_PATH, index=False)

    unresolved_df.to_csv(UNRESOLVED_PATH, index=False)

    ignored_df.to_csv(IGNORED_PATH, index=False)

    logger.info(f"Resolved exported: {len(resolved_df)}")

    logger.info(f"Unresolved exported: {len(unresolved_df)}")

    logger.info(f"Ignored exported: {len(ignored_df)}")
    