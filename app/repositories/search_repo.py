from sqlalchemy import text
from app.core.db import rows_to_dict

def search_table(conn, table, id_col, query, entity_type):
    search_query = text(f"""
        SELECT {id_col} AS id, name
        FROM yacht_db.{table}
                       
        WHERE name ILIKE :search
        ORDER BY name
                       
        LIMIT 10
    """)

    rows = rows_to_dict(conn.execute(search_query, {"search": query}))

    for r in rows:
        r["type"] = entity_type

    return rows

def search_entities(conn, query):
    search_term = f"%{query}%"

    return {
        "boats": search_table(conn, "boats", "id_boat", search_term, "boat"),
        "regattas": search_table(conn, "regattas", "id_regatta", search_term, "regatta"),
        "classes": search_table(conn, "boat_classes", "id_class", search_term, "class"),
        "clubs": search_table(conn, "clubs", "id_club", search_term, "club")
    }
