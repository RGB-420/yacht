import pandas as pd
import os

def export_unique_split_column_values(input_path: str, column: str):
    output_folder = "scraper/output/prenormalization_data"

    df = pd.read_csv(input_path, usecols=[column])

    values = (
        df[column]
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
        .replace("", pd.NA)
        .dropna()
        .unique()
    )

    result_df = pd.DataFrame(sorted(values), columns=[f"{column.lower()}_raw_name"])

    result_df[f"{column.lower()}_canonical_name"] = ""
    result_df["status"] = ""
    result_df["confidence"] = ""
    result_df["notes"] = ""

    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, f"{column.lower()}_unique.csv")

    result_df.to_csv(output_path, index=False)

    print(f"✔ Exportado {column} (split) → {output_path}")


def create_type_class_template(input_csv):
    output_folder = "scraper/output/prenormalization_data"

    df = pd.read_csv(input_csv, usecols=["Boat Type", "Class"])

    # Limpiar
    df["Boat Type"] = (
        df["Boat Type"]
        .dropna()
        .astype(str)
        .str.split(",")
    )

    # Expandir tipos múltiples
    df = df.explode("Boat Type")
    df["Boat Type"] = df["Boat Type"].str.strip()

    # Quitar filas vacías
    df = df.dropna(subset=["Boat Type"])

    # Obtener combinaciones reales
    df_unique = df.drop_duplicates()

    # Renombrar
    df_unique = df_unique.rename(columns={
        "Boat Type": "raw_type",
        "Class": "raw_class"
    })

    # Añadir columnas para normalización
    df_unique["canonical_type"] = ""
    df_unique["canonical_class"] = ""
    df_unique["status"] = ""
    df_unique["confidence"] = ""
    df_unique["notes"] = ""

    df_unique = df_unique.sort_values(by='raw_type')

    df_unique.to_csv(f"{output_folder}/type_class_unique.csv", index=False)