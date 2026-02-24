import pandas as pd
import re

from domain.mappings.class_mapping import class_mapping

"""
Class normalizer

- Normalizes boat classes using regex mapping
- Removes rating numbers (e.g. IRC 1.90)

IT ISN'T USED
"""

# ------ Main function ------
def finalize_class_column(df):
    if "Class"  not in df.columns:
        return df
    
    df["Class"] = (df["Class"].astype(str).str.strip().str.replace("\xa0", "", regex=False))

    df["Class"] = df["Class"].apply(normalize_class)

    return df

# ------ Utils ------
def normalize_class(value):
    if pd.isna(value) or str(value).strip().lower() in {"", "nan"}:
        return None

    # Normalización básica
    text = value.upper().strip()

    # Quitar ratings numéricos (1.90, 2.15, etc.)
    text = re.sub(r"\b\d+(\.\d+)?\b", "", text).strip()

    # Aplicar mapping
    for normalized, patterns in class_mapping.items():
        for pattern in patterns:
            try:
                if re.search(pattern, text):
                    return normalized
            except re.error as e:
                print(f"Regex inválido: {pattern}")
                raise e

    return None
