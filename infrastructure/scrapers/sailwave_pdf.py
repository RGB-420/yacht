import camelot
import pandas as pd
from pathlib import Path

columns_map = {
    "owner": ["owner"],
    "boat": ["yacht", "boat"],
    "number": ["sail number", "sailno", "number"],
    "club": ["club"]
}

def normalize(col):
    return (
        str(col)
        .lower()
        .strip()
        .replace("\n", " ")
        .replace("\r", " ")
        .replace(".", "")
        .replace("_", " ")
        .replace("-", " ")
        .replace("  ", " ")
    )

def map_columns(df, columns_map):
    new_cols = []

    for col in df.columns:
        norm_col = normalize(col)
        mapped = col  # por defecto se queda igual

        for canonical, aliases in columns_map.items():
            if norm_col in aliases:
                mapped = canonical
                break

        new_cols.append(mapped)

    df.columns = new_cols
    return df

def scrape(route):
    route = Path(route)

    tables = camelot.read_pdf(
        str(route),
        pages="all",
        flavor="stream"
    )

    dfs = []

    for table in tables:
        df = table.df.reset_index(drop=True)

        header_idx = None
        for i, row in df.iterrows():
            row_norm = row.astype(str).apply(normalize)
            if any(val in columns_map["number"] for val in row_norm):
                header_idx = i
                break

        if header_idx is None:
            continue

        df.columns = df.iloc[header_idx]
        df = df.iloc[header_idx + 1:].reset_index(drop=True)

        df = map_columns(df, columns_map)

        df = df[df["number"].astype(str).str.contains(r"\d+", na=False)]

        dfs.append(df)

    if not dfs:
        raise ValueError("No se pudieron extraer tablas del PDF")

    df_all = pd.concat(dfs, ignore_index=True)

    expected = ["number", "boat", "owner", "club"]
    available = [c for c in expected if c in df_all.columns]
    df_all = df_all[available]

    return df_all