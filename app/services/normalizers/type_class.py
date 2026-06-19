import pandas as pd
import re

from pathlib import Path

from app.repositories.class_type_aliases_repo import create_pending_class_type_alias, load_class_type_alias_cache 

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

SEEN_UNKNOWN_CLASSES = set()

RAW_ALIAS_CACHE = {}
NORMALIZED_ALIAS_CACHE = {}

def final_type_class_columns(df, conn):
    global MAPPED_CLASS_TYPES
    global UNMAPPED_CLASS_TYPES

    MAPPED_CLASS_TYPES = 0
    UNMAPPED_CLASS_TYPES = 0

    if "Class" not in df.columns and "Boat Type" not in df.columns:
        return df
    
    df["Class_raw"] = df["Class"]
    df["Type_raw"] = df["Boat Type"]

    df["Class"] = (df["Class"].astype(str).str.strip().str.replace("\xa0", "", regex=False))

    df["Class"] = df["Class"].apply(preprocess_class)

    logger.info(f"Classes mapped: {df['Class'].notna().sum()}")
    logger.info(f"Classes set to None: {df['Class'].isna().sum()}")

    df['Boat Type'] = df['Boat Type'].str.replace(r"\.$", "", regex=True)

    df["Boat Type"] = (df["Boat Type"].astype("string").str.strip().str.replace("\xa0", "", regex=False))

    df["Boat Type"] = df["Boat Type"].str.replace(r"\s+\d\.\d+$", "", regex=True)

    df["Boat Type"] = df["Boat Type"].apply(preprocess_type)

    changed_types = (df["Type_raw"].fillna("") != df["Boat Type"].fillna("")).sum()

    logger.info(f"Boat types normalized: {changed_types}")

    df["Class_norm"] = df["Class"]
    df["Type_norm"] = df["Boat Type"]

    global RAW_ALIAS_CACHE
    global NORMALIZED_ALIAS_CACHE

    RAW_ALIAS_CACHE, NORMALIZED_ALIAS_CACHE = load_class_type_alias_cache(conn)

    df[["Class", "Boat Type"]] = df.apply(
        lambda row: pd.Series(
            map_or_collect_class_type(
                conn,
                row["Class_raw"],
                row["Type_raw"],
                row["Class_norm"],
                row["Type_norm"]
            )
        ),
        axis=1
    )

    df = df.drop(columns=["Class_raw", "Type_raw", "Class_norm", "Type_norm"])

    logger.info(f"Mapped class/type pairs: {MAPPED_CLASS_TYPES}")
    logger.info(f"Unmapped class/type pairs: {UNMAPPED_CLASS_TYPES}")

    return df

def preprocess_class(value):
    if pd.isna(value) or str(value).strip().lower() in {"", "nan"}:
        return None

    return str(value).upper().strip()

def preprocess_type(value):
    if pd.isna(value) or str(value).strip() in {"","0",'""'}:
        return None
    
    value = clean_type_string(value)

    for func in [normalize_j_boat, normalize_jpk_boat, normalize_x_boat]:
        result = func(value)
        if result:
            return result

    return value

def clean_type_string(n):
    n = n.upper().strip()
    n = re.sub(r"[‐-‒–—−]", "-", n)
    n = re.sub(r"\.+$", "", n)
    n = re.sub(r"\s+\d\.\d+", "", n)
    n = re.sub(r"\b(RUD|FRA|EU|US)\b", "", n)
    n = re.sub(r"\b(YACTH?|IMX|SPORT|OD|AP|PBFE|RUDD|MK\d)\b", "", n)
    n = re.sub(r"\s+", " ", n)

    return n

J_REGEX = re.compile(r"\bJ\s*/?\s*(\d{2,3})(S|E)?\b")

def normalize_j_boat(value):
    if not value:
        return None
    
    match = J_REGEX.search(value)
    if not match:
        return None
    
    number = match.group(1)
    suffix = match.group(2) or ""

    return f"J/{number}{suffix}"

JPK_REGEX = re.compile(r"\bJPK\s*(\d{1,2}\.\d{1,2}|\d{3,4})\b")

JPK_MAP = {
    "1010": "10.10",
    "1030": "10.30",
    "1050": "10.50",
    "1080": "10.80",
    "1090": "10.90",
    "1180": "11.80",
    "960": "9.60"
}

def normalize_jpk_boat(value):
    if not value:
        return None
    
    match = JPK_REGEX.search(value)
    if not match:
        return None
    
    raw = match.group(1)

    if "." in raw:
        model = raw
    else:
        model = JPK_MAP.get(raw)

    if not model:
        return None
    
    return f"JPK {model}"

X_REGEX = re.compile(r"\bX[\s/-]?(\d{2,3}|\d/\d|\d\.\d)\b")

X_MAP = {
    "3/4": "X-3/4",
    "332": "X-332",
    "35": "X-35",
    "302": "X-302",
    "34": "X-34",
    "362": "X-362",
    "37": "X-37",
    "372": "X-372",
    "40": "X-40",
    "95": "X-95",
    "99": "X-99",
    "55": "X-55"
}

def normalize_x_boat(value):
    if not value:
        return None

    match = X_REGEX.search(value)
    if not match:
        return None
    
    raw = match.group(1)

    model = X_MAP.get(raw)
    if not model:
        return None
    
    return model

def map_or_collect_class_type(conn, class_raw, type_raw, class_norm, type_norm):
    if pd.isna(class_norm) and pd.isna(type_norm):
        return None, None

    class_norm = str(class_norm).strip().upper() if pd.notna(class_norm) else None

    type_norm = str(type_norm).strip().upper() if pd.notna(type_norm) else None

    raw_key = (str(class_raw).strip().upper() if pd.notna(class_raw) else None,
               str(type_raw).strip().upper() if pd.notna(type_raw) else None)
    
    normalized_key = (class_norm, type_norm)

    global MAPPED_CLASS_TYPES
    global UNMAPPED_CLASS_TYPES

    entry = RAW_ALIAS_CACHE.get(raw_key)

    if entry is None:
        entry = NORMALIZED_ALIAS_CACHE.get(normalized_key)

    if entry is not None:
        status = entry["status"]

        if status == "resolved":
            MAPPED_CLASS_TYPES += 1

            return (entry["canonical_class"], entry["canonical_type"])
        
        elif status in ["pending", "unresolved", "ignored"]:
            return None, None
        
    UNMAPPED_CLASS_TYPES += 1

    logger.info(f"Creating pending class/type alias: {class_norm} | {type_norm}")

    create_pending_class_type_alias(conn, class_raw, type_raw, class_norm, type_norm)

    RAW_ALIAS_CACHE[raw_key] = {"status": "pending"}
    NORMALIZED_ALIAS_CACHE[normalized_key] = {"status": "pending"}

    return None, None

def fill_type_from_class(row):
    class_val = row["Class"]
    type_val = row["Boat Type"]

    if pd.isna(type_val) or str(type_val).strip() in {"", "nan", "None"}:
        if not (pd.isna(class_val) or str(class_val).strip() in {"", "nan", "None"}):
            return class_val
    
    return type_val
