import pandas as pd
import os

column_mapping = {
    "Boat": "Name",
    "boat_name": "Name",
    "boat": "Name",
    "name": "Name",
    "yacht_name": "Name",
    "Yacht": "Name",
    "class": "Class", 
    "Class Cowes Wk": "Class", 
    "class_name": "Class",
    "Type": "Boat Type",
    "type": "Boat Type",
    "yacht_type": "Boat Type",
    "boat_type": "Boat Type",
    "Design": "Boat Type",
    "owner": "Owner",
    "owner_name": "Owner",
    "No Sail": "Boat Id",
    "sail_number": "Boat Id",
    "boat_number": "Boat Id",
    "Boat Number": "Boat Id",
    "sailno": "Boat Id",
    "sail_no": "Boat Id",
    "Sail No": "Boat Id",
    "Sail No.": "Boat Id",
    "Sail Number": "Boat Id",
    "yacht_club":"Club",
    "club":"Club",
    "Yacht Club": "Club",
    "Team Name": "Club"
}

def read_csv(archivos):
    dfs = []

    for archivo in archivos:
        df = pd.read_csv(archivo)
        print(archivo)
        
        df = df.rename(columns=column_mapping)

        if "Boat Id" in df.columns:
            df["Boat Id"] = df["Boat Id"].astype("string")

        if "mna" in df.columns:
            df["mna"] = df["mna"].astype("string")
            mask = df["mna"].notna()
            df.loc[mask, "Boat Id"] = df.loc[mask, "mna"] + df.loc[mask, "Boat Id"]

        df["Source"] = os.path.splitext(os.path.basename(archivo))[0]

        dfs.append(df)

    for archivo, df in zip(archivos, dfs):
        if df.columns.duplicated().any():
            print("Columnas duplicadas en:", archivo)
            print(df.columns[df.columns.duplicated()])

    df_concat = pd.concat(dfs, ignore_index=True)

    df_concat = df_concat.drop_duplicates(subset=["Boat Id", "Name", "Class"])

    return df_concat