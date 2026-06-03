import pandas as pd

from app.core.config import DATA_MAPPING

from app.repositories.clubs_norm_repo import load_club_norm_cache
from app.repositories.club_aliases_repo import bulk_upsert_club_aliases, load_club_alias_cache

from app.services.normalizers.clubs import normalize_club

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

CLUB_MAPPING_PATH = DATA_MAPPING / "club_mapping_review.csv"

def sync_club_mapping(conn):

    logger.info("Syncing club mapping...")

    df = pd.read_csv(CLUB_MAPPING_PATH)

    logger.info(f"Rows loaded: {len(df)}")

    for col in df.columns:
        df[col] = df[col].astype("string").str.strip()

    df = df.replace(r"^\s*$", pd.NA, regex=True)

    df = df[df["club_raw_name"].notna()].copy()

    df = df[
        df["status"].isin([
            "resolved",
            "unresolved",
            "pending"
        ])
    ].copy()

    synced = 0
    skipped = 0

    club_norm_cache = load_club_norm_cache(conn)

    logger.info(f"Club norm cache: {len(club_norm_cache)}")

    existing_alias_cache, _ = load_club_alias_cache(conn)

    logger.info(f"Existing alias cache: {len(existing_alias_cache)}")

    payload = []

    for row in df.itertuples(index=False):
        raw_name = row.club_raw_name
        canonical_name = row.club_canonical_name
        status = row.status
        confidence = row.confidence

        if pd.isna(confidence):
            confidence = None

        id_club = None

        if status == "resolved" and pd.notna(canonical_name):
            id_club = club_norm_cache.get(
                str(canonical_name).upper()
            )

            if id_club is None:
                skipped += 1
                continue

        normalized_name = normalize_club(raw_name)

        existing = existing_alias_cache.get(str(raw_name).upper())

        if existing:
            existing_canonical = existing["canonical_name"]

            if (
                existing["normalized_name"] == normalized_name
                and existing["status"] == status
                and str(existing["confidence"]) == str(confidence)
                and str(existing_canonical) == str(canonical_name)
            ):
                continue

        payload.append({
            "raw_name": raw_name,
            "normalized_name": normalized_name,
            "id_club": id_club,
            "status": status,
            "confidence": confidence
        })
    
    if payload:
        bulk_upsert_club_aliases(conn, payload)

    synced = len(payload)

    logger.info(f"Aliases synced: {synced}")
    logger.info(f"Skipped: {skipped}")