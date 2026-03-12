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
        SELECT bc.id_class, bc.name, bc.manufacturer, bc.category, bc.rating_rule,
            COUNT(b.id_boat) AS number_of_boats
        FROM yacht_db.edition_classes ec
                 
        JOIN yacht_db.boat_classes bc
            ON ec.id_class = bc.id_class
        LEFT JOIN yacht_db.boat_type bt
            ON bt.id_class = bc.id_class
        LEFT JOIN yacht_db.boats b
            ON b.id_type = bt.id_type
        LEFT JOIN yacht_db.boat_editions be
            ON be.id_boat = b.id_boat
            AND be.id_edition = ec.id_edition
                 
        WHERE ec.id_edition = :edition_id
                 
        GROUP BY bc.id_class, bc.name, bc.manufacturer, bc.category, bc.rating_rule
                 
        ORDER BY bc.name
    """)

    result = conn.execute(query, {"edition_id": edition_id})

    return rows_to_dict(result)