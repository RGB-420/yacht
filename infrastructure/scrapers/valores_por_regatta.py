import pandas as pd
import glob
import os
import re

ruta = "CSV Regatas"
archivos = glob.glob(os.path.join(ruta, "*.csv"))

columnas_finales = ["Name", "Class", "Boat Type", "Owner", "Boat Number", "Club"]

column_mapping = {
    "Boat": "Name",
    "boat_name": "Name",
    "boat": "Name",
    "name": "Name",
    "yacht_name": "Name",
    "class": "Class", 
    "class_name": "Class",
    "Type": "Boat Type",
    "type": "Boat Type",
    "yacht_type": "Boat Type",
    "boat_type": "Boat Type",
    "owner": "Owner",
    "owner_name": "Owner",
    "No Sail": "Boat Number",
    "sail_number": "Boat Number",
    "sailno": "Boat Number",
    "Sail No": "Boat Number",
    "yacht_club":"Club",
    "club":"Club"
}

resumen = []

for archivo in archivos:
    df = pd.read_csv(archivo)
    print(os.path.basename(archivo))

    df = df.rename(columns=column_mapping)

    # Caso especial
    if os.path.basename(archivo) in ["Flying 15 National.csv", "J-Cup.csv", "RSrnYC Series Black.csv", "RSrnYC Series White.csv"]:
        df["Boat Number"] = df["mna"].astype(str) + df["Boat Number"].astype(str)

    fila = {"csv_name": os.path.basename(archivo)}

    for col in columnas_finales:
        if col in df.columns:
            fila[col] = df[col].dropna().count()
        else:
            fila[col] = 0

    resumen.append(fila)

df_final = pd.DataFrame(resumen)

fila_total = {"csv_name": "Total"}

for col in columnas_finales:
    fila_total[col] = df_final[col].sum()

df_final = pd.concat(
    [df_final, pd.DataFrame([fila_total])],
    ignore_index=True
)

df_final.to_csv("resumen_regatas.csv", index=False)