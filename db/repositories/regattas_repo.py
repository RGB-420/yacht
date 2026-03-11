from sqlalchemy import text

from utils.db_utils import rows_to_dict, row_to_dict

def upsert_regatta(conn, name, type=None, club_id=None, location_id=None):
    query = text("""
        INSERT INTO yacht_db.regattas (name, type, id_club, id_location)
        VALUES (:name, :type, :club_id, :location_id)

        ON CONFLICT (name)
        DO UPDATE SET
            type = EXCLUDED.type,
            id_club = COALESCE(EXCLUDED.id_club, yacht_db.regattas.id_club),
            id_location = COALESCE(EXCLUDED.id_location, yacht_db.regattas.id_location)

        RETURNING id_regatta;
    """)

    result = conn.execute(query, {"name": name, "type": type, "club_id": club_id, "location_id": location_id}).fetchone()

    return result[0], True

def get_regattas(conn):
    query = text("""
        SELECT r.id_regatta, r.name, r.type, c.name AS club_name, l.city, l.region, l.country
        FROM yacht_db.regattas r
        
        LEFT JOIN yacht_db.clubs c
            ON r.id_club = c.id_club
        LEFT JOIN yacht_db.locations l
            ON r.id_location = l.id_location
                 
        ORDER BY name
    """)

    result = conn.execute(query)

    return rows_to_dict(result)

def get_regatta_by_id(conn, regatta_id):
    query = text("""
        SELECT r.id_regatta, r.name, r.type, c.name AS club_name, l.city, l.region, l.country
        FROM yacht_db.regattas r
                 
        LEFT JOIN yacht_db.clubs c
            ON r.id_club = c.id_club
        LEFT JOIN yacht_db.locations l
            ON r.id_location = l.id_location
                 
        WHERE r.id_regatta = :id
                 
        ORDER BY name
    """)

    result = conn.execute(query, {"id": regatta_id}).fetchone()

    return row_to_dict(result)
