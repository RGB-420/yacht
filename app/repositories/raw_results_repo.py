from sqlalchemy import text
import pandas as pd

from psycopg2.extras import Json

def get_all_raw_results(conn):
    query = text("""
        SELECT regatta_name, year, raw_data
        FROM yacht_raw.raw_regatta_results
    """)

    result = conn.execute(query).fetchall()

    rows = []

    for regatta_name, year, data in result:
        for row in data:
            row["Source"] = f"{regatta_name}-{year}"
            rows.append(row)

    return pd.DataFrame(rows)

def insert_raw_result(conn, source_type, source_page, regatta_name, year, data):
    query = text("""
        INSERT INTO yacht_raw.raw_regatta_results 
            (source_type, source_page, regatta_name, year, raw_data)
                 
        VALUES (:source_type, :source_page, :regatta_name, :year, :data)
    """)

    conn.execute(query, {"source_type": source_type, "source_page": source_page, "regatta_name": regatta_name, "year": year, "data": Json(data)})