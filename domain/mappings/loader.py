import pandas as pd
from pathlib import Path

def load_simple_mapping(filename, key_col, value_col):
    path = Path(__file__).parent / filename
    df = pd.read_csv(path)

    df[key_col] = df[key_col].astype(str).str.strip()
    df[value_col] = df[value_col].astype(str).str.strip()

    return dict(zip(df[key_col], df[value_col]))

def load_regex_mapping(filename, pattern, value_col):
    path = Path(__file__).parent / filename
    df = pd.read_csv(path)

    df[value_col] = df[value_col].astype(str).str.strip()

    df[pattern] = (df[pattern].replace({pd.NA:None}).apply(lambda x: None if pd.isna(x) or x =="" else str(x).strip()))

    return list(zip(df[pattern], df[value_col]))

def load_regex_grouped_mapping(filename, pattern, value_col):
    path = Path(__file__).parent / filename
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

    path = Path(__file__).parent / filename
    df = pd.read_csv(path)

    for col in raw_cols + canonical_cols:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in CSV")

        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan":None, "": None})

    df = df[df[raw_cols].notna().any(axis=1)]

    mapping = {}

    for _, row in df.iterrows():
        raw_key = tuple(row[col] for col in raw_cols)
        canonical_value = tuple(row[col] for col in canonical_cols)
        mapping[raw_key] = canonical_value

    return mapping