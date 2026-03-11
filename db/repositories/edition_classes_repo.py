from sqlalchemy import text

from utils.db_utils import rows_to_dict

def insert_edition_class(conn, edition_id, class_id):
    query = text("""
        INSERT INTO yacht_db.edition_classes (id_edition, id_class)
        VALUES (:edition_id, :class_id)
                 
        ON CONFLICT (id_edition, id_class) DO NOTHING;
    """)

    conn.execute(query, {"edition_id": edition_id, "class_id": class_id})

def get_edition_classes(conn, edition_id):
    query = text("""
        SELECT bc.id_class, bc.name, bc.manufacturer, bc.category, bc.rating_rule
        FROM yacht_db.edition_classes ec
        JOIN yacht_db.boat_classes bc
            ON ec.id_class = bc.id_class
        WHERE ec.id_edition = :edition_id
        ORDER BY bc.name
    """)

    result = conn.execute(query, {"edition_id": edition_id})

    return rows_to_dict(result)