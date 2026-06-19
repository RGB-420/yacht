from sqlalchemy import text

from app.core.db import rows_to_dict

def insert_boat_edition(conn, boat_id, edition_id):
    query = text("""
        INSERT INTO yacht_db.boat_editions (id_boat, id_edition)
        VALUES (:boat_id, :edition_id)
                 
        ON CONFLICT (id_boat, id_edition)
        DO NOTHING;
    """)

    conn.execute(query, {"boat_id": boat_id, "edition_id": edition_id})

def get_edition_boats(conn, edition_id):
    query = text("""
        SELECT b.id_boat, b.name, b.boat_identifier,
            ARRAY_REMOVE(ARRAY_AGG(DISTINCT bc.id_class), NULL) AS class_ids,
            ARRAY_REMOVE(ARRAY_AGG(DISTINCT bc.name), NULL) AS classes
        FROM yacht_db.boat_editions be
                 
        JOIN yacht_db.boats b
            ON be.id_boat = b.id_boat
        LEFT JOIN yacht_db.boat_type_relations btr
            ON btr.id_boat = b.id_boat
        LEFT JOIN yacht_db.boat_type bt
            ON bt.id_type = btr.id_type
        LEFT JOIN yacht_db.boat_classes bc
            ON bt.id_class = bc.id_class
                 
        WHERE be.id_edition = :edition_id
                 
        GROUP BY b.id_boat, b.name, b.boat_identifier
                 
        ORDER BY b.name
    """)

    result = conn.execute(query, {"edition_id": edition_id})

    return rows_to_dict(result)

def get_boats_edition(conn, boat_id):
    query = text("""
        SELECT re.id_edition, re.year, r.id_regatta, r.name AS regatta_name, l.city, l.region, l.country
        FROM yacht_db.boat_editions be
        
        JOIN yacht_db.regatta_editions re
            ON be.id_edition = re.id_edition
        JOIN yacht_db.regattas r
            ON re.id_regatta = r.id_regatta
        LEFT JOIN yacht_db.locations l
            ON l.id_location = r.id_location
        
        WHERE be.id_boat = :boat_id
        ORDER BY re.year DESC
    """)

    result = conn.execute(query, {"boat_id": boat_id})

    return rows_to_dict(result)

def load_boat_editions_rel_cache(conn):
    query = text("""
        SELECT id_boat, id_edition
        FROM yacht_db.boat_editions
    """)

    rows = conn.execute(query).fetchall()

    return {
        (row.id_boat, row.id_edition)
        for row in rows
    }
