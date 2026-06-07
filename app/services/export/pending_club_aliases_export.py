import pandas as pd

from rapidfuzz import process, fuzz
from pathlib import Path

from app.repositories.club_aliases_repo import get_pending_club_aliases, get_resolved_club_aliases
from app.repositories.clubs_norm_repo import get_all_canonical_clubs

from pipelines.common.logger import get_logger

logger = get_logger(__name__)


OUTPUT_DIR = Path("data/review")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DEBUG_FILE = OUTPUT_DIR / "pending_club_aliases.csv"
MAPPING_FILE = OUTPUT_DIR / "club_mapping_pending.csv"

def export_pending_club_aliases(conn):
    logger.info("Exporting pending club aliases...")

    rows = get_pending_club_aliases(conn)

    resolved_aliases = get_resolved_club_aliases(conn)

    canonical_clubs = get_all_canonical_clubs(conn)
    
    resolved_normalized = [r["normalized_name"] for r in resolved_aliases]

    if not rows:
        logger.info("No pending aliases found")
        return
    
    for row in rows:
        normalized = row["normalized_name"]

        if not normalized:
            continue

        alias_match = process.extractOne(
            normalized,
            resolved_normalized,
            scorer=fuzz.token_sort_ratio
        )

        if alias_match:
            alias_name, alias_score, alias_idx = alias_match

            matched_alias = resolved_aliases[alias_idx]

            row["alias_suggested_canonical"] = (matched_alias["canonical_name"])

            row["alias_score"] = alias_score

        else:
            row["alias_suggested_canonical"] = None
            row["alias_score"] = None

        canonical_match = process.extractOne(
            normalized,
            canonical_clubs,
            scorer=fuzz.token_sort_ratio
        )

        if canonical_match:
            canonical_name, canonical_score, _ = canonical_match

            row["canonical_suggested"] = canonical_name
            row["canonical_score"] = canonical_score
        
        else:
            row["canonical_suggested"] = None
            row["canonical_score"] = None

    df_debug = pd.DataFrame(rows)

    df_debug = df_debug.sort_values(by=["alias_score", "canonical_score", "occurrences"], ascending=[False, False, False], na_position="last")

    df_debug.to_csv(DEBUG_FILE, index=False)

    logger.info(f"Debug aliases exported: {len(df_debug)}")

    logger.info(f"Saved debug file: {DEBUG_FILE}")

    export_rows = []

    for row in rows:
        suggested = (row.get("alias_suggested_canonical") or row.get("canonical_suggested"))

        confidence = (row.get("alias_score") or row.get("canonical_score"))

        if pd.notna(confidence) and confidence > 75:
            export_rows.append({
                "club_raw_name": row["raw_name"],
                "club_canonical_name": suggested,
                "status": "pending",
                "confidence": confidence,
                "notes": ""
            })
        else:
            export_rows.append({
                "club_raw_name": row["raw_name"],
                "club_canonical_name": row["normalized_name"].title() if pd.notna(row["normalized_name"]) else row["raw_name"].title(),
                "status": "pending",
                "confidence": "",
                "notes": ""
            })
    
    df_mapping = pd.DataFrame(export_rows)

    df_mapping = df_mapping.drop_duplicates(subset=["club_raw_name"])

    df_mapping = df_mapping.sort_values(
        by=["confidence", "club_raw_name"],
        ascending=[False, True],
        na_position="last"
    )

    df_mapping.to_csv(MAPPING_FILE, index=False)

    logger.info(f"Mapping review exported: {len(df_mapping)}")

    logger.info(f"Saved debug file: {MAPPING_FILE}")
    