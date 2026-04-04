import pandas as pd
from pathlib import Path

from app.core.config import DATA_MAPPING

def load_simple_mapping(filename, raw_col, canonical_col):
    path = f"{DATA_MAPPING}/{filename}"
    df = pd.read_csv(path)

    df = df[df[raw_col].astype(str).str.strip() != ""]

    df[raw_col] = df[raw_col].astype(str).str.strip().str.upper()
    df[canonical_col] = df[canonical_col].astype("string").str.strip()

    mapping = {}

    for _, row in df.iterrows():
        key = row[raw_col]

        mapping[key] = {
            "canonical": row[canonical_col] if pd.notna(row[canonical_col]) else None,
            "status": row["status"],
            "confidence": row.get("confidence")
        }

    return mapping

def load_regex_mapping(filename, pattern, value_col):
    path = f"{DATA_MAPPING}/{filename}"
    df = pd.read_csv(path)

    df[value_col] = df[value_col].astype(str).str.strip()

    df[pattern] = (df[pattern].replace({pd.NA:None}).apply(lambda x: None if pd.isna(x) or x =="" else str(x).strip()))

    return list(zip(df[pattern], df[value_col]))

def load_regex_grouped_mapping(filename, pattern, value_col):
    path = f"{DATA_MAPPING}/{filename}"
    df = pd.read_csv(path)

    df[value_col] = df[value_col].astype(str).str.strip()

    df[pattern] = df[pattern].astype(str).str.strip()

    mapping = {}

    for _,row in df.iterrows():
        canonical = row[value_col]
        regex_pattern = row[pattern]

        if canonical not in mapping:
            mapping[canonical] = []

        mapping[canonical].append(regex_pattern)
    
    return mapping

def load_dual_mapping(filename, raw_cols, canonical_cols):
    if len(raw_cols) != len(canonical_cols):
        raise ValueError("raw_cols and canonical_cols must have the same length")

    path = f"{DATA_MAPPING}/{filename}"
    df = pd.read_csv(path)

    for col in raw_cols + canonical_cols:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in CSV")

        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan":None, "": None})

    df = df[df[raw_cols].notna().any(axis=1)]

    df = df[df["status"] == 'resolved']

    mapping = {}

    for _, row in df.iterrows():
        raw_key = tuple(row[col] for col in raw_cols)
        canonical_value = tuple(row[col] for col in canonical_cols)
        mapping[raw_key] = canonical_value

    return mapping