from sqlalchemy import text

from utils.db_utils import rows_to_dict

def upsert_boat_type(conn, name, class_id):
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

def get_class_types(conn, class_id):
    query = text("""
        SELECT id_type, name
        FROM yacht_db.boat_type
                 
        WHERE id_class = :class_id
        ORDER BY name
    """)

    result = conn.execute(query, {"class_id": class_id})

    return rows_to_dict(result)