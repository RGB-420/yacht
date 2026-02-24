import pandas as pd

cols_to_parse = ["Name", "Owner", "Club", "Source"]

def parse_list_cell(x):
    if pd.isna(x) or str(x).strip() == "":
        return []
    return [v.strip() for v in str(x).split(",") if v.strip()]

def parse_list_columns(df):
    for col in cols_to_parse:
        if col in df.columns:
            df[col] = df[col].apply(parse_list_cell)
    return df

def explode_owners(df):
    rows = []

    for _, row in df.iterrows():
        boats = row["Name"] if row["Name"] else [None]
        owners = row["Owner"]
        clubs = row["Club"] if row["Club"] else [None]
        sources = row["Source"] if row["Source"] else [None]

        for boat in boats:
            for owner in owners:
                for club in clubs:
                    rows.append({
                        "Owner": owner,
                        "Boat": boat,
                        "Club": club,
                        "Source": sources
                    })

    return pd.DataFrame(rows)

def clean_strings(df):
    df = df.replace({"None": None, "NONE": None, "nan": None, "NaN": None})

    for col in ["Owner", "Boat", "Club"]:
        df[col] = (
            df[col]
            .apply(lambda x: x.strip() if isinstance(x, str) else x)
            .replace("", None)
        )

    return df

def infer_club_from_owner(df):
    mask = (
        df["Owner"].str.contains("club", case=False, na=False)
        & df["Club"].isna()
    )

    df.loc[mask, "Club"] = df.loc[mask, "Owner"]
    df.loc[mask, "Owner"] = None

    return df

def master(df):
    df = df.copy()

    df = parse_list_columns(df)
    df_owners = explode_owners(df)

    df_owners = clean_strings(df_owners)
    df_owners = infer_club_from_owner(df_owners)

    df_owners = df_owners.drop_duplicates(
        subset=["Owner", "Boat", "Club"]
    )

    return df_owners