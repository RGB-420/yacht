import pandas as pd

"""
Boat ID normalizer

- Cleans boat identifier
- Extracts numeric boat number for grouping
"""

# ------ Main function -------
def finalize_boat_id_column(df):     
    if "Boat Id" not in df.columns:
        return df
    
    df["Boat Id"] = (df["Boat Id"].astype(str).str.replace(r"\s+", "", regex=True))

    df["Boat Number"] = df["Boat Id"].str.extract(r"(\d+)")

    df["Boat Number"] = df["Boat Number"].astype("Int64")

    return df