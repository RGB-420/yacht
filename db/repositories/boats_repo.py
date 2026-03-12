from sqlalchemy import text

from utils.db_utils import row_to_dict, rows_to_dict

def upsert_boat(conn, name, boat_identifier, type_id=None):
    query = text("""
        INSERT INTO yacht_db.boats (name, boat_identifier, id_type)
        VALUES (:name, :boat_identifier, :type_id)
                 
        ON CONFLICT (name, boat_identifier) DO UPDATE SET
            id_type = COALESCE(EXCLUDED.id_type, yacht_db.boats.id_type)
                 
        RETURNING id_boat, (xmax = 0) AS inserted;
    """)

    result = conn.execute(query, {"name": name, "boat_identifier": boat_identifier, "type_id": type_id}).fetchone()

    return result[0], result[1]

def get_boats(conn):
    query = text("""
        SELECT b.id_boat, b.name, b.boat_identifier, bc.id_class, bc.name AS class_name, bt.id_type, bt.name AS type_name,
                ARRAY_REMOVE(ARRAY_AGG(DISTINCT o.name), NULL) AS owners,
                ARRAY_REMOVE(ARRAY_AGG(DISTINCT c.name), NULL) AS clubs
        FROM yacht_db.boats b
                 
        LEFT JOIN yacht_db.boat_type bt
            ON bt.id_type = b.id_type
        LEFT JOIN yacht_db.boat_classes bc
            ON bt.id_class = bc.id_class
        LEFT JOIN yacht_db.boats_owner bo
            ON b.id_boat = bo.id_boat
        LEFT JOIN yacht_db.owners o
            ON bo.id_owner = o.id_owner
        LEFT JOIN yacht_db.boat_clubs bclu
            ON b.id_boat = bclu.id_boat
        LEFT JOIN yacht_db.clubs c
            ON bclu.id_club = c.id_club
                 
        GROUP BY b.id_boat, b.name, b.boat_identifier, bc.id_class, bc.name, bt.id_type, bt.name
                 
        ORDER BY b.name
    """)

    result = conn.execute(query)

    return rows_to_dict(result)

def get_boat_by_id(conn, boat_id):
    query = text("""
        SELECT b.id_boat, b.name, b.boat_identifier, bc.id_class, bc.name AS class_name, bt.id_type, bt.name AS type_name,
                ARRAY_REMOVE(ARRAY_AGG(DISTINCT o.name), NULL) AS owners,
                ARRAY_REMOVE(ARRAY_AGG(DISTINCT c.name), NULL) AS clubs
        FROM yacht_db.boats b
                 
        LEFT JOIN yacht_db.boat_type bt
            ON bt.id_type = b.id_type
        LEFT JOIN yacht_db.boat_classes bc
            ON bt.id_class = bc.id_class
        LEFT JOIN yacht_db.boats_owner bo
            ON b.id_boat = bo.id_boat
        LEFT JOIN yacht_db.owners o
            ON bo.id_owner = o.id_owner
        LEFT JOIN yacht_db.boat_clubs bclu
            ON b.id_boat = bclu.id_boat
        LEFT JOIN yacht_db.clubs c
            ON bclu.id_club = c.id_club
                 
        WHERE b.id_boat = :boat_id
        GROUP BY b.id_boat, b.name, b.boat_identifier, bc.id_class, bc.name, bt.id_type, bt.name
    """)

    result = conn.execute(query, {"boat_id": boat_id}).fetchone()

    return row_to_dict(result)

def get_class_boats(conn, class_id):
    query = text("""
        SELECT b.id_boat, b.name, b.boat_identifier,
            ARRAY_REMOVE(ARRAY_AGG(DISTINCT o.name), NULL) AS owners
        FROM yacht_db.boats b
        
        JOIN yacht_db.boat_type bt
            ON b.id_type = bt.id_type
        LEFT JOIN yacht_db.boats_owner bo
            ON bo.id_boat = b.id_boat
        LEFT JOIN yacht_db.owners o
            ON o.id_owner = bo.id_owner
                
        WHERE bt.id_class = :class_id

        GROUP BY b.id_boat, b.name, b.boat_identifier
                         
        ORDER BY b.name
    """)

    result = conn.execute(query, {"class_id": class_id})

    return rows_to_dict(result)
