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
        SELECT id_regatta, name, type, id_club, id_location, created_at
        FROM yacht_db.regattas
        ORDER BY name
    """)

    result = conn.execute(query)

    return rows_to_dict(result)

def get_regatta_by_id(conn, regatta_id):
    query = text("""
        SELECT id_regatta, name, type, id_club, id_location, created_at
        FROM yacht_db.regattas 
        WHERE id_regatta = :id
    """)

    result = conn.execute(query, {"id": regatta_id}).fetchone()

    return row_to_dict(result)
