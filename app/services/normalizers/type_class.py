import pandas as pd
import re

from pathlib import Path

from app.services.mappings.type_class_mapping import type_class_mapping
from app.services.mappings.class_mapping import class_mapping

from pipelines.common.logger import get_logger

logger = get_logger(__name__)

PRENORM_PATH = Path("data/prenormalization/class_type_prenormalization.csv")

SEEN_PRENORM = set()

EXISTING_PRENORM = set()
NEW_PRENORM_ROWS = []

if PRENORM_PATH.exists() and PRENORM_PATH.stat().st_size > 0:

    try:
        df_existing = pd.read_csv(PRENORM_PATH)

        EXISTING_PRENORM = set((df_existing["raw_class"].fillna("").str.lower() + "|" + df_existing["raw_type"].fillna("").str.lower()))

    except Exception:
        EXISTING_PRENORM = set()

SEEN_UNKNOWN_CLASSES = set()


def final_type_class_columns(df):
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

    df[["Class", "Boat Type"]] = df.apply(
        lambda row: pd.Series(
            map_or_collect_class_type(
                row["Class_norm"],
                row["Type_norm"]
            )
        ),
        axis=1
    )

    df = df.drop(columns=["Class_raw", "Type_raw", "Class_norm", "Type_norm"])

    logger.info(f"Mapped class/type pairs: {MAPPED_CLASS_TYPES}")
    logger.info(f"Unmapped class/type pairs: {UNMAPPED_CLASS_TYPES}")

    flush_class_type_prenorm()

    return df

def preprocess_class(value):
    if pd.isna(value) or str(value).strip().lower() in {"", "nan"}:
        return None

    # Normalización básica
    text = value.upper().strip()

    for normalized, patterns in class_mapping.items():
        for pattern in patterns:
            try:
                if re.search(pattern, text):
                    return normalized
            except re.error as e:
                print(f"Regex invalido: {pattern}")
                raise e
    
    if text not in SEEN_UNKNOWN_CLASSES:
        logger.warning(f"Unknown class not mapped: {text}")
        SEEN_UNKNOWN_CLASSES.add(text)

    return None

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

def map_or_collect_class_type(class_norm, type_norm):
    if pd.isna(class_norm) and pd.isna(type_norm):
        return None, None

    key = (class_norm, type_norm)

    mapping = type_class_mapping.get(key)

    if mapping:
        global MAPPED_CLASS_TYPES
        MAPPED_CLASS_TYPES += 1
        return mapping["canonical_class"], mapping["canonical_type"]

    save_class_type_prenorm(class_norm, type_norm)

    global UNMAPPED_CLASS_TYPES
    UNMAPPED_CLASS_TYPES += 1

    return class_norm, type_norm

def fill_type_from_class(row):
    class_val = row["Class"]
    type_val = row["Boat Type"]

    if pd.isna(type_val) or str(type_val).strip() in {"", "nan", "None"}:
        if not (pd.isna(class_val) or str(class_val).strip() in {"", "nan", "None"}):
            return class_val
    
    return type_val


def save_class_type_prenorm(raw_class, raw_type):
    if pd.isna(raw_class) and pd.isna(raw_type):
        return

    key = f"{str(raw_class).lower()}|{str(raw_type).lower()}"

    if key in SEEN_PRENORM:
        return
    
    if key in EXISTING_PRENORM:
        return
    
    SEEN_PRENORM.add(key)
    EXISTING_PRENORM.add(key)

    NEW_PRENORM_ROWS.append({
        "raw_class": raw_class,
        "raw_type": raw_type,
        "canonical_type": "",
        "canonical_class": "",
        "status": "pending",
        "confidence": "",
        "notes": ""
    })

def flush_class_type_prenorm():

    if not NEW_PRENORM_ROWS:
        return

    df_new = pd.DataFrame(NEW_PRENORM_ROWS)

    if PRENORM_PATH.exists() and PRENORM_PATH.stat().st_size > 0:

        try:
            df_existing = pd.read_csv(PRENORM_PATH)

        except Exception:

            df_existing = pd.DataFrame(columns=[
                "raw_class",
                "raw_type",
                "canonical_type",
                "canonical_class",
                "status",
                "confidence",
                "notes"
            ])

        df_final = pd.concat(
            [df_existing, df_new],
            ignore_index=True
        )

    else:

        df_final = df_new

    df_final.to_csv(PRENORM_PATH, index=False)

    logger.info(
        f"Saved {len(df_new)} new class/type prenorm rows"
    )

    NEW_PRENORM_ROWS.clear()