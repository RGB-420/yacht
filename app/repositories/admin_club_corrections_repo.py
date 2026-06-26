from pathlib import Path
from typing import Dict, Optional

import pandas as pd

from app.core.config import DATA_MAPPING, DATA_REVIEW


CLUB_MAPPING_REVIEW_PATH = DATA_MAPPING / "clubs/club_mapping_review.csv"
CLUB_MAPPING_PENDING_PATH = DATA_REVIEW / "club_mapping_pending.csv"
CLUB_MAPPING_RESOLVED_PATH = DATA_MAPPING / "clubs/club_mapping_resolved.csv"
CLUB_MAPPING_UNRESOLVED_PATH = DATA_MAPPING / "clubs/club_mapping_unresolved.csv"
CLUB_MAPPING_IGNORED_PATH = DATA_MAPPING / "clubs/club_mapping_ignored.csv"

CLUB_MAPPING_COLUMNS = [
    "club_raw_name",
    "club_canonical_name",
    "status",
    "confidence",
    "notes",
    "regatta",
]

EDITABLE_COLUMNS = {
    "club_canonical_name",
    "status",
    "confidence",
    "notes",
}

STATUS_OPTIONS = ["pending", "resolved", "unresolved", "ignored"]
SUGGESTION_OPTIONS = [
    "all",
    "with_suggestion",
    "without_suggestion",
    "high_numeric_confidence",
    "low_numeric_confidence",
]
SORT_OPTIONS = [
    "club_raw_name",
    "club_canonical_name",
    "regatta",
    "confidence",
    "status",
]
HIGH_CONFIDENCE_THRESHOLD = 80

WORKING_PATHS = {
    "pending": CLUB_MAPPING_PENDING_PATH,
    "resolved": CLUB_MAPPING_RESOLVED_PATH,
    "unresolved": CLUB_MAPPING_UNRESOLVED_PATH,
    "ignored": CLUB_MAPPING_IGNORED_PATH,
}


def _empty_dataframe():
    return pd.DataFrame(columns=CLUB_MAPPING_COLUMNS)


def _load_club_mapping_dataframe():
    if not Path(CLUB_MAPPING_REVIEW_PATH).exists():
        return _empty_dataframe()

    df = pd.read_csv(CLUB_MAPPING_REVIEW_PATH)

    for col in CLUB_MAPPING_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    return df[CLUB_MAPPING_COLUMNS]


def _records(df):
    clean_df = df.astype(object).where(pd.notna(df), None).copy()
    clean_df.insert(0, "row_id", clean_df.index.astype(int))

    return clean_df.to_dict(orient="records")


def get_club_corrections(
    limit: int,
    offset: int,
    status: Optional[str] = None,
    q: Optional[str] = None,
    suggestion: Optional[str] = None,
    sort_by: str = "club_raw_name",
    sort_dir: str = "asc",
):
    df = _load_club_mapping_dataframe()
    metrics = _build_metrics(df)

    if status and status != "all":
        df = df[df["status"].astype("string") == status].copy()

    if suggestion and suggestion != "all":
        has_suggestion = df["club_canonical_name"].apply(_has_value)
        numeric_confidence = pd.to_numeric(df["confidence"], errors="coerce")

        if suggestion == "with_suggestion":
            df = df[has_suggestion].copy()
        elif suggestion == "without_suggestion":
            df = df[~has_suggestion].copy()
        elif suggestion == "high_numeric_confidence":
            df = df[has_suggestion & (numeric_confidence >= HIGH_CONFIDENCE_THRESHOLD)].copy()
        elif suggestion == "low_numeric_confidence":
            df = df[has_suggestion & numeric_confidence.notna() & (numeric_confidence < HIGH_CONFIDENCE_THRESHOLD)].copy()

    if q:
        query = str(q).strip().lower()

        if query:
            searchable = (
                df["club_raw_name"].fillna("").astype(str)
                + " "
                + df["club_canonical_name"].fillna("").astype(str)
                + " "
                + df["regatta"].fillna("").astype(str)
            ).str.lower()

            df = df[searchable.str.contains(query, regex=False)].copy()

    df = _sort_dataframe(df, sort_by, sort_dir)

    total = len(df)
    page_df = df.iloc[offset:offset + limit]

    return {
        "data": _records(page_df),
        "total": total,
        "limit": limit,
        "offset": offset,
        "metrics": metrics,
    }


def update_club_correction(row_id: int, updates: Dict[str, Optional[str]]):
    df = _load_club_mapping_dataframe()

    if df.empty or row_id < 0 or row_id >= len(df):
        return None

    for col, value in updates.items():
        if col not in EDITABLE_COLUMNS:
            continue

        df.at[row_id, col] = value

    CLUB_MAPPING_REVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLUB_MAPPING_REVIEW_PATH, index=False)

    updated_row = df.loc[[row_id]]
    _sync_working_files(updated_row.iloc[0])

    return _records(updated_row)[0]


def _has_value(value):
    if pd.isna(value):
        return False

    return bool(str(value).strip())


def _clean_key_value(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    return value or None


def _row_key(row):
    return _clean_key_value(row["club_raw_name"])


def _sync_working_files(row):
    row_status = _clean_key_value(row["status"])
    row_payload = {
        col: (None if pd.isna(row[col]) else row[col])
        for col in CLUB_MAPPING_COLUMNS
    }
    row_key = _row_key(row)

    for status, path in WORKING_PATHS.items():
        working_df = _load_working_dataframe(path)

        if working_df.empty:
            matches = pd.Series([], dtype=bool)
        else:
            matches = working_df.apply(lambda current: _row_key(current) == row_key, axis=1)

        if status == row_status:
            if matches.any():
                working_df.loc[matches, CLUB_MAPPING_COLUMNS] = pd.DataFrame(
                    [row_payload] * int(matches.sum()),
                    index=working_df.index[matches],
                )
            else:
                working_df = pd.concat(
                    [working_df, pd.DataFrame([row_payload])],
                    ignore_index=True,
                )
        elif matches.any():
            working_df = working_df.loc[~matches].copy()

        working_df = working_df[CLUB_MAPPING_COLUMNS].sort_values(
            by=["club_raw_name"],
            na_position="last",
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        working_df.to_csv(path, index=False)


def _load_working_dataframe(path):
    if not Path(path).exists():
        return _empty_dataframe()

    df = pd.read_csv(path)

    for col in CLUB_MAPPING_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    return df[CLUB_MAPPING_COLUMNS]


def _sort_dataframe(df, sort_by: str, sort_dir: str):
    if sort_by not in SORT_OPTIONS:
        sort_by = "club_raw_name"

    ascending = sort_dir != "desc"

    if sort_by == "confidence":
        return (
            df.assign(_numeric_confidence=pd.to_numeric(df["confidence"], errors="coerce"))
            .sort_values(
                by=["_numeric_confidence", "club_raw_name"],
                ascending=[ascending, True],
                na_position="last",
            )
            .drop(columns=["_numeric_confidence"])
        )

    return df.sort_values(
        by=[sort_by, "club_raw_name"],
        ascending=[ascending, True],
        na_position="last",
        key=lambda col: col.fillna("").astype(str).str.lower(),
    )


def _build_metrics(df):
    has_suggestion = df["club_canonical_name"].apply(_has_value)
    numeric_confidence = pd.to_numeric(df["confidence"], errors="coerce")
    status_counts = df["status"].fillna("missing").astype(str).str.strip().value_counts()

    metrics = {
        "total": int(len(df)),
        "with_suggestion": int(has_suggestion.sum()),
        "without_suggestion": int((~has_suggestion).sum()),
        "high_numeric_confidence": int((has_suggestion & (numeric_confidence >= HIGH_CONFIDENCE_THRESHOLD)).sum()),
        "low_numeric_confidence": int((has_suggestion & numeric_confidence.notna() & (numeric_confidence < HIGH_CONFIDENCE_THRESHOLD)).sum()),
        "non_numeric_confidence": int((has_suggestion & df["confidence"].apply(_has_value) & numeric_confidence.isna()).sum()),
    }

    for status in STATUS_OPTIONS:
        metrics[status] = int(status_counts.get(status, 0))

    return metrics


def get_club_correction_options():
    return {
        "statuses": STATUS_OPTIONS,
        "suggestions": SUGGESTION_OPTIONS,
        "sorts": SORT_OPTIONS,
    }
