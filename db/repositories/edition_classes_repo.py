from sqlalchemy import text

def insert_edition_class(conn, edition_id, class_id):
    query = text("""
        INSERT INTO yacht_db.edition_classes (id_edition, id_class)
        VALUES (:edition_id, :class_id)
                 
        ON CONFLICT (id_edition, id_class) DO NOTHING;
    """)

    conn.execute(query, {"edition_id": edition_id, "class_id": class_id})
