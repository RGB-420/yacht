import pandas as pd
import re

from app.core.config import DATA_MAPPING

from app.repositories.clubs_norm_repo import upsert_norm_club

CLUBS_MAPPING_PATH = DATA_MAPPING / "club_mapping_review.csv"

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

def sync_club_norm(conn):
    logger.info("Syncing canonical clubs...")

    df = pd.read_csv(CLUBS_MAPPING_PATH)

    logger.info(f"Rows loaded: {len(df)}")

    for col in df.columns:
        df[col] = df[col].astype("string").str.strip()

    df = df.replace(r"^\s*$", pd.NA, regex=True)

    clubs_df = df[
        (df["status"] == "resolved")
        &
        (df["club_canonical_name"].notna())
    ].copy()

    clubs_df["club_canonical_name"] = (
        clubs_df["club_canonical_name"]
        .apply(split_canonical)
    )

    clubs_df = (
        clubs_df
        .explode("club_canonical_name")
        .reset_index(drop=True)
    )

    clubs_df = clubs_df[
        clubs_df["club_canonical_name"].apply(is_valid_canonical)
    ]

    clubs_df["club_canonical_name"] = (
        clubs_df["club_canonical_name"]
        .astype("string")
        .str.strip()
    )

    clubs_df["website"] = (
        clubs_df["club_canonical_name"]
        .apply(lambda x: get_single_website(clubs_df, x))
    )

    clubs_df = clubs_df.drop_duplicates(
        subset=["club_canonical_name"]
    )

    clubs_df = clubs_df.sort_values(
        "club_canonical_name"
    ).reset_index(drop=True)

    synced = 0    

    for row in clubs_df.itertuples(index=False):

        canonical_name = row.club_canonical_name
        website = row.website

        upsert_norm_club(
            conn=conn,
            canonical_name=canonical_name,
            website=website
        )

        synced += 1

    logger.info(f"Canonical clubs synced: {synced}")


def split_canonical(cell):

    if pd.isna(cell):
        return []

    parts = [
        p.strip()
        for p in str(cell).split("//")
        if p.strip()
    ]

    return list(dict.fromkeys(parts))

def is_valid_canonical(name):

    if pd.isna(name):
        return False

    name = str(name).strip()

    if len(name) <= 4:
        return False

    if re.fullmatch(r"[A-Z0-9& -]+", name):

        words = name.split()

        if all(len(w) <= 5 for w in words):
            return False

    return True


def extract_urls(text):

    if pd.isna(text):
        return []

    text = str(text)

    urls = re.findall(
        r"https?://[^\s,)]+",
        text
    )

    return list(dict.fromkeys(urls))


def get_single_website(df, canonical_name):

    rows = df[
        df["club_canonical_name"] == canonical_name
    ]

    urls = []

    for note in rows["notes"].dropna():

        urls.extend(
            extract_urls(note)
        )

    urls = list(dict.fromkeys(urls))

    if len(urls) == 1:
        return urls[0]

    return pd.NA