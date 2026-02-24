import pandas as pd

from rapidfuzz import fuzz


def group_boats(df, name_col="Name_clean", number_col="Boat Number"):
    df = df.copy()

    df["group_id"] = None
    group_id = 0

    df = df.sort_values([number_col, name_col])

    for boat_number, sub_df in df.groupby("Boat Number"):
        if pd.isna(boat_number):
            continue

        indices = sub_df.index.tolist()
        usados = set()

        for i in indices:
            if i in usados:
                continue

            group_id += 1
            df.loc[i, "group_id"] = group_id
            usados.add(i)

            a = df.loc[i, "Name_clean"]

            for j in indices:
                if j in usados:
                    continue

                b = df.loc[j, "Name_clean"]

                if abs(len(a) - len(b)) > 10:
                    continue

                if fuzz.token_sort_ratio(a, b) >= 80:
                    df.loc[j, "group_id"] = group_id
                    usados.add(j)

    return df