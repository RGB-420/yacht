import pandas as pd

def split_and_clean(value):
    if pd.isna(value):
        return []
    
    return [v.strip() for v in str(value).split(",") if v.strip()]

def explode_boats_for_db(df):
    rows = []

    for _, row in df.iterrows():
        owners = split_and_clean(row["Owner"])
        clubs = split_and_clean(row["Club"])
        sources = split_and_clean(row["Source"])


        if not owners:
            owners = [None]

        if not clubs:
            clubs = [None]

        if not sources:
            sources = [None]

        for owner in owners:
            for club in clubs:
                for source in sources:
                    new_row = row.copy()
                    new_row["Owner"] = owner
                    new_row["Club"] = club
                    new_row["Source"] = source

                    rows.append(new_row)

    return pd.DataFrame(rows)