from sqlalchemy import text

def find_club_by_canonical_name(conn, canonical_name):
    query = text("""
        SELECT id_club, canonical_name
        FROM yacht_norm.clubs
        WHERE UPPER(canonical_name) = UPPER(:canonical_name)
    """)

    result = conn.execute(query, {"canonical_name": canonical_name}).mappings().first()

    return result


def upsert_norm_club(conn, canonical_name, website=None):
    query = text("""
        INSERT INTO yacht_norm.clubs (canonical_name, website)
        VALUES (:canonical_name, :website)
                 
        ON CONFLICT (canonical_name)
        DO UPDATE SET 
            website= COALESCE(
                EXCLUDED.website,
                yacht_norm.clubs.website
            )
        
        RETURNING id_club
    """)

    result = conn.execute(query, {"canonical_name": canonical_name, "website": (None if website is None or str(website) == "<NA>" else website)})

    return result.scalar()


def get_all_canonical_clubs(conn):
    query = text("""
        SELECT canonical_name
        FROM yacht_norm.clubs
    """)

    result = conn.execute(query)

    return [row[0] for row in result]
