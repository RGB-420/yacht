from sqlalchemy import text

def upsert_club(conn, name, short_name=None, estimated_numbers=None, location_id=None):
    query = text("""
        INSERT INTO yacht_db.clubs (name, short_name, estimated_numbers, id_location)
        VALUES (:name, :short_name, :estimated_numbers, :location_id)
                 
        ON CONFLICT (name) DO UPDATE SET
            short_name = COALESCE(EXCLUDED.short_name, yacht_db.clubs.short_name),
            estimated_numbers = COALESCE(EXCLUDED.estimated_numbers, yacht_db.clubs.estimated_numbers),
            id_location = COALESCE(EXCLUDED.id_location, yacht_db.clubs.id_location)
                 
        RETURNING id_club, (xmax=0) AS inserted
    """)

    result = conn.execute(query, {"name": name, "short_name": short_name, "estimated_numbers": estimated_numbers, "location_id": location_id}).fetchone()

    return result[0], result[1]

def get_club_id(conn, name):
    query = text("""
        SELECT id_club FROM yacht_db.clubs
        WHERE name = :name
    """)

    result = conn.execute(query, {"name": name}).fetchone()

    return result[0] if result else None
