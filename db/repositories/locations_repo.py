from sqlalchemy import text

def upsert_location(conn, city, region, country):
    insert_query = text("""
        INSERT INTO yacht_db.locations (city, region, country)
        VALUES (:city, :region, :country)
                 
        ON CONFLICT (region, country, city)
            DO NOTHING
                 
        RETURNING id_location
    """)

    result = conn.execute(insert_query, {"city":city, "region": region, "country": country}).fetchone()

    if result:
        return[0], True

    select_query = text("""
        SELECT id_location
        FROM yacht_db.locations
        WHERE city = :city
            AND region = :region
            AND country = :country
    """)

    existing = conn.execute(select_query, {"city": city, "region": region, "country": country}).fetchone()

    return existing[0], False

