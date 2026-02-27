from sqlalchemy import text

def upsert_boat(conn, name, boat_identifier, class_id=None):
    query = text("""
        INSERT INTO yacht_db.boats (name, boat_identifier, id_class)
        VALUES (:name, :boat_identifier, :class_id, :club_id)
                 
        ON CONFLICT (name, boat_identifier) DO UPDATE SET
            id_class = COALESCE(EXCLUDED.id_class, yacht_db.boats.id_class)
                 
        RETURNING id_boat, (xmax = 0) AS inserted;
    """)

    result = conn.execute(query, {"name": name, "boat_identifier": boat_identifier, "class_id": class_id}).fetchone()

    return result[0], result[1]