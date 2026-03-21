import pandas as pd

from db.repositories.clubs_repo import get_all_clubs_with_location


def sync_clubs_csv_with_db(conn, df, csv_path):
    # 🔹 Obtener clubs de DB
    db_rows = get_all_clubs_with_location(conn)

    db_clubs = pd.DataFrame(
        db_rows,
        columns=["name", "short_name", "estimated_numbers", "city", "region", "country"]
    )

    # 🔹 Comparar nombres
    csv_names = set(df["name"])
    db_names = set(db_clubs["name"])

    new_names = db_names - csv_names
    new_clubs = db_clubs[db_clubs["name"].isin(new_names)]

    # 🔹 Actualizar CSV si hay nuevos
    if not new_clubs.empty:
        print(f"[INFO] {len(new_clubs)} new clubs found → adding to CSV")

        df_updated = pd.concat([df, new_clubs], ignore_index=True)
        df_updated.to_csv(csv_path, index=False)

    else:
        print("[INFO] No new clubs found")