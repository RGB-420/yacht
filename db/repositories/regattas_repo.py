from sqlalchemy import text

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