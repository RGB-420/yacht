from pathlib import Path
from typing import Dict, Optional

import pandas as pd

from app.core.config import DATA_MAPPING, DATA_REVIEW


CLASS_TYPE_REVIEW_PATH = DATA_MAPPING / "class_types/class_type_review.csv"
CLASS_TYPE_PENDING_PATH = DATA_REVIEW / "class_type_pending.csv"
CLASS_TYPE_RESOLVED_PATH = DATA_MAPPING / "class_types/class_type_resolved.csv"
CLASS_TYPE_UNRESOLVED_PATH = DATA_MAPPING / "class_types/class_type_unresolved.csv"
CLASS_TYPE_IGNORED_PATH = DATA_MAPPING / "class_types/class_type_ignored.csv"

CLASS_TYPE_COLUMNS = [
    "raw_class",
    "raw_type",
    "canonical_type",
    "canonical_class",
    "status",
    "confidence",
    "notes",
]

EDITABLE_COLUMNS = {
    "canonical_class",
    "canonical_type",
    "status",
    "confidence",
    "notes",
}

STATUS_OPTIONS = ["pending", "resolved", "unresolved", "ignored"]
SHAPE_OPTIONS = [
    "all",
    "missing_any_raw",
    "missing_raw_class",
    "missing_raw_type",
    "has_both_raw",
]
SORT_OPTIONS = [
    "raw_class",
    "raw_type",
    "canonical_class",
    "canonical_type",
    "confidence",
    "status",
]

SPLIT_PATHS = {
    "pending": CLASS_TYPE_PENDING_PATH,
    "resolved": CLASS_TYPE_RESOLVED_PATH,
    "unresolved": CLASS_TYPE_UNRESOLVED_PATH,
    "ignored": CLASS_TYPE_IGNORED_PATH,
}


def _empty_dataframe():
    return pd.DataFrame(columns=CLASS_TYPE_COLUMNS)


def _load_class_type_dataframe():
    if not Path(CLASS_TYPE_REVIEW_PATH).exists():
        return _empty_dataframe()

    df = pd.read_csv(CLASS_TYPE_REVIEW_PATH)

    for col in CLASS_TYPE_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    return df[CLASS_TYPE_COLUMNS]


def _clean_key_value(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    return value or None


def _row_key(row):
    return (
        _clean_key_value(row["raw_class"]),
        _clean_key_value(row["raw_type"]),
    )


def _records(df):
    clean_df = df.astype(object).where(pd.notna(df), None).copy()
    clean_df.insert(0, "row_id", clean_df.index.astype(int))

    return clean_df.to_dict(orient="records")


def get_class_type_corrections(
    limit: int,
    offset: int,
    status: Optional[str] = None,
    q: Optional[str] = None,
    shape: Optional[str] = None,
    sort_by: str = "raw_class",
    sort_dir: str = "asc",
):
    df = _load_class_type_dataframe()
    metrics = _build_metrics(df)

    if status and status != "all":
        df = df[df["status"].astype("string") == status].copy()

    if shape and shape != "all":
        raw_class_present = df["raw_class"].apply(_has_value)
        raw_type_present = df["raw_type"].apply(_has_value)

        if shape == "missing_any_raw":
            df = df[~raw_class_present | ~raw_type_present].copy()
        elif shape == "missing_raw_class":
            df = df[~raw_class_present].copy()
        elif shape == "missing_raw_type":
            df = df[~raw_type_present].copy()
        elif shape == "has_both_raw":
            df = df[raw_class_present & raw_type_present].copy()

    if q:
        query = str(q).strip().lower()

        if query:
            searchable = (
                df["raw_class"].fillna("").astype(str)
                + " "
                + df["raw_type"].fillna("").astype(str)
                + " "
                + df["canonical_class"].fillna("").astype(str)
                + " "
                + df["canonical_type"].fillna("").astype(str)
                + " "
                + df["notes"].fillna("").astype(str)
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


def update_class_type_correction(row_id: int, updates: Dict[str, Optional[str]]):
    df = _load_class_type_dataframe()

    if df.empty or row_id < 0 or row_id >= len(df):
        return None

    for col, value in updates.items():
        if col not in EDITABLE_COLUMNS:
            continue

        df.at[row_id, col] = value

    CLASS_TYPE_REVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLASS_TYPE_REVIEW_PATH, index=False)

    updated_row = df.loc[[row_id]]
    _sync_split_files(updated_row.iloc[0])

    return _records(updated_row)[0]


def _sync_split_files(row):
    row_status = _clean_key_value(row["status"])
    row_payload = {
        col: (None if pd.isna(row[col]) else row[col])
        for col in CLASS_TYPE_COLUMNS
    }
    row_key = _row_key(row)

    for status, path in SPLIT_PATHS.items():
        split_df = _load_split_dataframe(path)

        if split_df.empty:
            matches = pd.Series([], dtype=bool)
        else:
            matches = split_df.apply(lambda current: _row_key(current) == row_key, axis=1)

        if status == row_status:
            if matches.any():
                split_df.loc[matches, CLASS_TYPE_COLUMNS] = pd.DataFrame(
                    [row_payload] * int(matches.sum()),
                    index=split_df.index[matches],
                )
            else:
                split_df = pd.concat(
                    [split_df, pd.DataFrame([row_payload])],
                    ignore_index=True,
                )
        elif matches.any():
            split_df = split_df.loc[~matches].copy()

        split_df = split_df[CLASS_TYPE_COLUMNS].sort_values(
            by=["raw_class", "raw_type"],
            na_position="last",
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        split_df.to_csv(path, index=False)


def _load_split_dataframe(path):
    if not Path(path).exists():
        return _empty_dataframe()

    df = pd.read_csv(path)

    for col in CLASS_TYPE_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    return df[CLASS_TYPE_COLUMNS]


def _has_value(value):
    return _clean_key_value(value) is not None


def _sort_dataframe(df, sort_by: str, sort_dir: str):
    if sort_by not in SORT_OPTIONS:
        sort_by = "raw_class"

    ascending = sort_dir != "desc"

    if sort_by == "confidence":
        return (
            df.assign(_numeric_confidence=pd.to_numeric(df["confidence"], errors="coerce"))
            .sort_values(
                by=["_numeric_confidence", "raw_class", "raw_type"],
                ascending=[ascending, True, True],
                na_position="last",
            )
            .drop(columns=["_numeric_confidence"])
        )

    return df.sort_values(
        by=[sort_by, "raw_class", "raw_type"],
        ascending=[ascending, True, True],
        na_position="last",
        key=lambda col: col.fillna("").astype(str).str.lower(),
    )


def _build_metrics(df):
    raw_class_present = df["raw_class"].apply(_has_value)
    raw_type_present = df["raw_type"].apply(_has_value)
    canonical_class_present = df["canonical_class"].apply(_has_value)
    canonical_type_present = df["canonical_type"].apply(_has_value)
    numeric_confidence = pd.to_numeric(df["confidence"], errors="coerce")
    status_counts = df["status"].fillna("missing").astype(str).str.strip().value_counts()

    metrics = {
        "total": int(len(df)),
        "missing_any_raw": int((~raw_class_present | ~raw_type_present).sum()),
        "missing_raw_class": int((~raw_class_present).sum()),
        "missing_raw_type": int((~raw_type_present).sum()),
        "has_both_raw": int((raw_class_present & raw_type_present).sum()),
        "with_canonical_class": int(canonical_class_present.sum()),
        "with_canonical_type": int(canonical_type_present.sum()),
        "with_both_canonical": int((canonical_class_present & canonical_type_present).sum()),
        "missing_any_canonical": int((~canonical_class_present | ~canonical_type_present).sum()),
        "numeric_confidence": int(numeric_confidence.notna().sum()),
        "non_numeric_confidence": int((df["confidence"].apply(_has_value) & numeric_confidence.isna()).sum()),
    }

    for status in STATUS_OPTIONS:
        metrics[status] = int(status_counts.get(status, 0))

    return metrics


def get_class_type_correction_options():
    return {
        "statuses": STATUS_OPTIONS,
        "shapes": SHAPE_OPTIONS,
        "sorts": SORT_OPTIONS,
    }
