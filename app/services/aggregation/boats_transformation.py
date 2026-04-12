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
        classes = split_and_clean(row["Class"])
        types = split_and_clean(row["Boat Type"])


        if not owners:
            owners = [None]

        if not clubs:
            clubs = [None]

        if not sources:
            sources = [None]

        if not classes:
            classes = [None]

        if not types:
            types = [None]

        for owner in owners:
            for club in clubs:
                for source in sources:
                    for class_ in classes:
                        for type in types:
                            new_row = row.copy()
                            new_row["Owner"] = owner
                            new_row["Club"] = club
                            new_row["Source"] = source
                            new_row["Class"] = class_
                            new_row["Boat Type"] = type

                            rows.append(new_row)

    return pd.DataFrame(rows)