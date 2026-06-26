from pathlib import Path
from typing import Dict, Optional

import pandas as pd

from app.core.config import DATA_MAPPING, DATA_PRENORM


OWNER_PRENORM_PATH = DATA_PRENORM / "owner_prenormalization.csv"
OWNER_MAPPING_PATH = DATA_MAPPING / "owner_mapping.csv"

OWNER_PRENORM_COLUMNS = [
    "raw_name",
    "canonical_name",
    "status",
    "confidence",
    "entity_type",
    "notes",
]

OWNER_MAPPING_COLUMNS = [
    "raw_name",
    "canonical_name",
    "confidence",
    "notes",
]

EDITABLE_COLUMNS = {
    "canonical_name",
    "status",
    "confidence",
    "entity_type",
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
    "raw_name",
    "canonical_name",
    "confidence",
    "entity_type",
    "status",
]
HIGH_CONFIDENCE_THRESHOLD = 90


def _empty_prenorm_dataframe():
    return pd.DataFrame(columns=OWNER_PRENORM_COLUMNS)


def _empty_mapping_dataframe():
    return pd.DataFrame(columns=OWNER_MAPPING_COLUMNS)


def _load_owner_prenorm_dataframe():
    if not Path(OWNER_PRENORM_PATH).exists():
        return _empty_prenorm_dataframe()

    df = pd.read_csv(OWNER_PRENORM_PATH)

    for col in OWNER_PRENORM_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    return df[OWNER_PRENORM_COLUMNS].astype(object)


def _records(df):
    clean_df = df.astype(object).where(pd.notna(df), None).copy()

    for col in OWNER_PRENORM_COLUMNS:
        clean_df[col] = clean_df[col].apply(_string_or_none)

    clean_df.insert(0, "row_id", clean_df.index.astype(int))

    return clean_df.to_dict(orient="records")


def get_owner_corrections(
    limit: int,
    offset: int,
    status: Optional[str] = None,
    entity_type: Optional[str] = None,
    suggestion: Optional[str] = None,
    q: Optional[str] = None,
    sort_by: str = "raw_name",
    sort_dir: str = "asc",
):
    df = _load_owner_prenorm_dataframe()
    metrics = _build_metrics(df)

    if status and status != "all":
        df = df[df["status"].astype("string") == status].copy()

    if entity_type and entity_type != "all":
        df = df[df["entity_type"].astype("string") == entity_type].copy()

    if suggestion and suggestion != "all":
        has_suggestion = df["canonical_name"].apply(_has_value)
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
                df["raw_name"].fillna("").astype(str)
                + " "
                + df["canonical_name"].fillna("").astype(str)
                + " "
                + df["entity_type"].fillna("").astype(str)
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


def update_owner_correction(row_id: int, updates: Dict[str, Optional[str]]):
    df = _load_owner_prenorm_dataframe()

    if df.empty or row_id < 0 or row_id >= len(df):
        return None

    for col, value in updates.items():
        if col not in EDITABLE_COLUMNS:
            continue

        df.at[row_id, col] = value

    OWNER_PRENORM_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OWNER_PRENORM_PATH, index=False)

    updated_row = df.loc[[row_id]]
    _sync_owner_mapping(updated_row.iloc[0])

    return _records(updated_row)[0]


def _sync_owner_mapping(row):
    raw_name = _clean_key_value(row["raw_name"])

    if raw_name is None:
        return

    mapping_df = _load_owner_mapping_dataframe()

    matches = mapping_df["raw_name"].apply(_clean_key_value) == raw_name
    status = _clean_key_value(row["status"])
    canonical_name = _clean_key_value(row["canonical_name"])

    if status == "resolved" and canonical_name is not None:
        row_payload = {
            "raw_name": raw_name,
            "canonical_name": canonical_name,
            "confidence": None if pd.isna(row["confidence"]) else row["confidence"],
            "notes": None if pd.isna(row["notes"]) else row["notes"],
        }

        if matches.any():
            mapping_df.loc[matches, OWNER_MAPPING_COLUMNS] = pd.DataFrame(
                [row_payload] * int(matches.sum()),
                index=mapping_df.index[matches],
            )
        else:
            mapping_df = pd.concat(
                [mapping_df, pd.DataFrame([row_payload])],
                ignore_index=True,
            )
    elif matches.any():
        mapping_df = mapping_df.loc[~matches].copy()

    mapping_df = mapping_df[OWNER_MAPPING_COLUMNS].sort_values(
        by=["raw_name"],
        na_position="last",
        key=lambda col: col.fillna("").astype(str).str.lower(),
    )
    OWNER_MAPPING_PATH.parent.mkdir(parents=True, exist_ok=True)
    mapping_df.to_csv(OWNER_MAPPING_PATH, index=False)


def _load_owner_mapping_dataframe():
    if not Path(OWNER_MAPPING_PATH).exists():
        return _empty_mapping_dataframe()

    df = pd.read_csv(OWNER_MAPPING_PATH)

    for col in OWNER_MAPPING_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    return df[OWNER_MAPPING_COLUMNS].astype(object)


def _has_value(value):
    if pd.isna(value):
        return False

    return bool(str(value).strip())


def _clean_key_value(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    return value or None


def _string_or_none(value):
    if pd.isna(value):
        return None

    return str(value)


def _sort_dataframe(df, sort_by: str, sort_dir: str):
    if sort_by not in SORT_OPTIONS:
        sort_by = "raw_name"

    ascending = sort_dir != "desc"

    if sort_by == "confidence":
        return (
            df.assign(_numeric_confidence=pd.to_numeric(df["confidence"], errors="coerce"))
            .sort_values(
                by=["_numeric_confidence", "raw_name"],
                ascending=[ascending, True],
                na_position="last",
            )
            .drop(columns=["_numeric_confidence"])
        )

    return df.sort_values(
        by=[sort_by, "raw_name"],
        ascending=[ascending, True],
        na_position="last",
        key=lambda col: col.fillna("").astype(str).str.lower(),
    )


def _build_metrics(df):
    has_suggestion = df["canonical_name"].apply(_has_value)
    numeric_confidence = pd.to_numeric(df["confidence"], errors="coerce")
    status_counts = df["status"].fillna("missing").astype(str).str.strip().value_counts()
    entity_type_counts = df["entity_type"].fillna("missing").astype(str).str.strip().value_counts()

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

    for entity_type in _entity_type_options(df):
        metrics[f"entity_type_{entity_type.lower()}"] = int(entity_type_counts.get(entity_type, 0))

    return metrics


def _entity_type_options(df):
    values = (
        df["entity_type"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    return sorted(value for value in values.unique() if value)


def get_owner_correction_options():
    df = _load_owner_prenorm_dataframe()

    return {
        "statuses": STATUS_OPTIONS,
        "entity_types": _entity_type_options(df),
        "suggestions": SUGGESTION_OPTIONS,
        "sorts": SORT_OPTIONS,
    }
