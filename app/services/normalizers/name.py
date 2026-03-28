import re
import pandas as pd

"""
Name normalizer

- Creates auxiliary column 'Name_clean' for fuzzy matching
- 'Name_clean' is not part of the final output
"""

# ------ Main function ------
def finalize_name_column(df):
    if "Name" not in df.columns:
        return df

    df["Name"] = df["Name"].str.title()

    df["Name"] = (df["Name"].str.replace("'", "", regex=False).str.replace("-", "", regex=False).str.replace("  ", " ", regex=False).str.strip())

    df["Name"] = (df["Name"].str.replace(r"\s*\(\s*Corinthian\s*\)", "", regex=True).str.strip())

    df["Name_clean"] = df["Name"].apply(normalize_name_for_match)

    return df

# ------ Utils ------
def normalize_name_for_match(s):
    if pd.isna(s):
        return ""
    s = s.upper()
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s