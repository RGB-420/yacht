import pandas as pd

from pathlib import Path

from app.core.config import DATA_MAPPING

from app.repositories.clubs_norm_repo import find_club_by_canonical_name
from app.repositories.club_aliases_repo import upsert_club_alias

from app.services.normalizers.clubs import normalize_club

CLUB_MAPPING_PATH = DATA_MAPPING / "club_mapping_review.csv"

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

def sync_club_mapping(conn):

    logger.info("Syncing club mapping...")

    df = pd.read_csv(CLUB_MAPPING_PATH)

    logger.info(f"Rows loaded: {len(df)}")

    for col in df.columns:
        df[col] = df[col].astype("string").str.strip()

    df = df.replace(r"^\s*$", pd.NA, regex=True)

    df = df[
        df["status"].isin([
            "resolved",
            "unresolved",
            "pending"
        ])
    ].copy()

    synced = 0
    skipped = 0

    for row in df.itertuples(index=False):
        raw_name = row.club_raw_name
        canonical_name = row.club_canonical_name
        status = row.status
        confidence = row.confidence

        if pd.isna(confidence):
            confidence = None

        id_club = None

        if status == "resolved" and pd.notna(canonical_name):
            club = find_club_by_canonical_name(
                conn,
                canonical_name
            )

            if club is None:
                skipped += 1
                continue
            
            id_club = club["id_club"]

        normalized_name = normalize_club(raw_name)

        upsert_club_alias(
                conn=conn,
                raw_name=raw_name,
                normalized_name=normalized_name,
                id_club=id_club,
                status=status,
                confidence=confidence
            )
    
        synced += 1
    
    logger.info(f"Aliases synced: {synced}")
    logger.info(f"Skipped: {skipped}")