import pandas as pd

def list_to_csv_cell(values):
    if isinstance(values, list):
        return ", ".join(values)
    return values

def upper_class_list(values):
    if not isinstance(values, list):
        return values
    return [v for v in values if isinstance(v, str)]


def aggregate_boat_groups(df, final_columns):
    df = df.sort_values(by="Boat Number")
    
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            print(f"Columna con listas: {col}")

    df_grouped = (df.groupby("group_id", as_index=False).agg(lambda x: list(pd.unique(x.dropna()))))

    df_grouped["Class"] = df_grouped["Class"].apply(upper_class_list)

    for col in final_columns:
        df_grouped[col] = df_grouped[col].apply(list_to_csv_cell)

    df_grouped["Boat Id"] = (
        df_grouped["Boat Id"]
        .apply(lambda x: max([s.strip() for s in x.split(",")], key=len) if isinstance(x, str) else x)
    )

    df_grouped["Name"] = (
        df_grouped["Name"]
        .apply(lambda x: max([s.strip() for s in x.split(",")], key=len) if isinstance(x, str) else x)
    )

    return df_grouped