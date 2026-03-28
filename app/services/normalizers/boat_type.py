import pandas as pd
import re

from app.services.mappings.class_mapping import class_mapping
"""
Boat Type normalizer

- Identifies and normalizes boat models
- Prioritizes specific brands (J, JPK, X)
- Falls back to regex-based type mapping
"""

# ------ Main function ------
def finalize_boat_type_column(df):
    if "Boat Type" not in df.columns:
        return df
    
    df['Boat Type'] = df['Boat Type'].str.replace(r"\.$", "", regex=True)

    df["Boat Type"] = (
        df["Boat Type"]
        .astype("string")
        .str.strip()
        .str.replace("\xa0", "", regex=False)
    )

    df["Boat Type"] = df["Boat Type"].str.replace(
        r"\s+\d\.\d+$", "", regex=True
    )

    #df['Boat Type'] = df["Boat Type"].apply(normalize_boat_type)

    return df


# ------ Utils ------
MODIFIERS = [
    "CUSTOM", "MODIFIED", "MOD", "SHALLOW DRAFT",
    "WB", "FIN", "KEEL", "HULL", "APPENDAGES"
]

J_REGEX = re.compile(r"\bJ\s*/?\s*(\d{2,3})(S|E)?\b")
JPK_REGEX = re.compile(r"\bJPK\s*(\d{1,2}\.\d{1,2}|\d{3,4})\b")
X_REGEX = re.compile(r"\bX\s*/?\s*-?\s*(\d{2,3}|\d/\d|\d\.\d)\b")

def clean_type_string(n):
    n = n.upper().strip()
    n = re.sub(r"[‐-‒–—−]", "-", n)
    n = re.sub(r"\.+$", "", n)              
    n = re.sub(r"\s+\d\.\d+", "", n)           
    n = re.sub(r"\b(RUD|FRA|EU|US)\b", "", n) 
    n = re.sub(r"\b(YACHTS?|IMX|SPORT|OD|AP|PBFE|RUDD|MK\d)\b", "", n)
    n = re.sub(r"\s+", " ", n)
    return n

"""def normalize_boat_type(name):
    if pd.isna(name) or str(name).strip() in {"", "0", '""'}:
        return None

    j_type = normalize_j_boat(name)
    if j_type:
        return j_type
    
    jpk_type = normalize_jpk_boat(name)
    if jpk_type:
        return jpk_type
    
    x_type = normalize_x_boat(name)
    if x_type:
        return x_type

    n = name.upper()
    n = re.sub(r"[^\w\s/\.]", " ", n)
    n = re.sub(r"\s+", " ", n)

    for m in MODIFIERS:
        n = n.replace(m, "")

    return n


# J-Boats                
def normalize_j_boat(name):
    if not name:
        return None

    n = clean_type_string(name)
    
    match = J_REGEX.search(n)
    if not match:
        return None

    number = match.group(1)
    suffix = match.group(2) or ""

    return f"J/{number}{suffix}"

# JPK Boats
JPK_MAP = {
    "1010": "10.10",
    "1030": "10.30",
    "1050": "10.50",
    "1080": "10.80",
    "1090": "10.90",
    "1180": "11.80",
    "960":  "9.60",
}

def normalize_jpk_boat(name):
    if not name:
        return None

    n = clean_type_string(name)
    
    match = JPK_REGEX.search(n)
    if not match:
        return None

    raw = match.group(1)

    # Normaliza formato
    if "." in raw:
        model = raw
    else:
        model = JPK_MAP.get(raw)

    if not model:
        return None

    return f"JPK {model}"

# X Boats
X_MAP = {
    "3/4": "X-3/4",
    "332": "X-332",
    "35":  "X-35",
    "302": "X-302",
    "34":  "X-34",
    "362":  "X-362",
    "37":  "X-37",
    "372":  "X-372",
    "40":  "X-40",
    "95":  "X-95",
    "99":  "X-99",
    "55":  "X-55",
}

def normalize_x_boat(name):
    if not name:
        return None
    
    n = clean_type_string(name)
    n = re.sub(r"\bX(?=\d)", "X ", n)

    match = X_REGEX.search(n)
    if not match:
        return None

    raw = match.group(1)

    model = X_MAP.get(raw)
    if not model:
        return None

    return model"""