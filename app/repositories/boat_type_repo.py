from sqlalchemy import text

from app.core.db import rows_to_dict

def upsert_boat_type(conn, name, class_id):
    if class_id is not None:
        insert_query = text("""
            INSERT INTO yacht_db.boat_type (name, id_class)
            VALUES (:name, :class_id)
            
            ON CONFLICT (name, id_class) DO NOTHING
                            
            RETURNING id_type
        """)

        result = conn.execute(insert_query, {"name": name, "class_id": class_id}).fetchone()

        if result:
            return result[0], True
        
        select_query = text("""
            SELECT id_type FROM yacht_db.boat_type
            WHERE name = :name
                AND id_class = :class_id
        """)

        existing = conn.execute(select_query, {"name": name, "class_id": class_id}).fetchone()

        return existing[0], False
    
    else:
        select_query = text("""
            SELECT id_type FROM yacht_db.boat_type
            WHERE name = :name AND id_class IS NULL
        """)

        existing = conn.execute(select_query, {"name": name}).fetchone()

        if existing:
            return existing[0], False

        insert_query = text("""
            INSERT INTO yacht_db.boat_type (name, id_class)
            VALUES (:name, NULL)
            RETURNING id_type
        """)

        result = conn.execute(insert_query, {"name": name}).fetchone()

        return result[0], True

def load_type_cache(conn):
    query = text("""
        SELECT id_type, name, id_class
        FROM yacht_db.boat_type
    """)

    result = conn.execute(query)

    rows = rows_to_dict(result)

    return {
        (
            row["name"],
            row["id_class"]
        ): row["id_type"]
        for row in rows
    }

def get_class_types(conn, class_id):
    query = text("""
        SELECT id_type, name
        FROM yacht_db.boat_type
                 
        WHERE id_class = :class_id
        ORDER BY name
    """)

    result = conn.execute(query, {"class_id": class_id})

    return rows_to_dict(result)