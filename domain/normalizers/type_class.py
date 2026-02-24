import pandas as pd
import re

from domain.mappings.type_class_mapping import type_class_mapping
from domain.mappings.class_mapping import class_mapping

def final_type_class_columns(df):
    if "Class" not in df.columns and "Boat Type" not in df.columns:
        return df
    
    df["Class"] = (df["Class"].astype(str).str.strip().str.replace("\xa0", "", regex=False))

    df["Class"] = df["Class"].apply(preprocess_class)

    df['Boat Type'] = df['Boat Type'].str.replace(r"\.$", "", regex=True)

    df["Boat Type"] = (df["Boat Type"].astype("string").str.strip().str.replace("\xa0", "", regex=False))

    df["Boat Type"] = df["Boat Type"].str.replace(r"\s+\d\.\d+$", "", regex=True)

    df["Boat Type"] = df["Boat Type"].apply(preprocess_type)

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