import numpy as np

def coalesce_columns(df, new_col, candidates):
    if new_col not in df.columns:
        df[new_col] = np.nan

    for col in candidates:
        if col in df.columns:
            df[new_col] = df[new_col].fillna(df[col])

    return df

keep_cols = ["Name", "Class", "Boat Type", "Owner", "Boat Id", "Club", "Source"]

def normalize_columns(df):
    COLUMN_MAPPING = {
        "Name": ["Boat", "boat_name", "boat", "name", "yacht_name", "Yacht"],
        "Class": ["class", "Class Cowes Wk", "class_name"],
        "Boat Type": ["Type", "type", "yacht_type", "boat_type", "Design"],
        "Owner": ["owner", "owner_name"],
        "Boat Id": [
            "No Sail", "sail_number", "boat_number", "Boat Number",
            "sailno", "sail_no", "Sail No", "Sail No.", "Sail Number"
        ],
        "Club": ["yacht_club", "club", "Yacht Club", "Team Name"]
    }

    df.columns = df.columns.str.strip()

    for target, sources in COLUMN_MAPPING.items():
        df = coalesce_columns(df, target, sources)

    if "mna" in df.columns:
        df["Boat Id"] = df["Boat Id"].fillna("")
        df["mna"] = df["mna"].fillna("")

        mask = df["mna"] != ""
        df.loc[mask, "Boat Id"] = df.loc[mask, "mna"] + df.loc[mask, "Boat Id"]

    return df[keep_cols]