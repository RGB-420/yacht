from sqlalchemy import text

def get_or_create_location(conn, city, region, country):
    select_query = text("""
        SELECT id_location
        FROM yacht_db.locations
        WHERE city = :city
            AND region = :region
            AND country = :country
    """)

    result = conn.execute(select_query, {"city": city, "region": region, "country": country}).fetchone()

    if result:
        return result[0], False
    
    insert_query = text("""
        INSERT INTO yacht_db.locations (city, region, country)
        VALUES (:city, :region, :country)
                 
        ON CONFLICT (region, country, city)
            DO NOTHING
                 
        RETURNING id_location
    """)

    insert_result = conn.execute(insert_query, {"city": city, "region": region, "country": country}).fetchone()

    return insert_result[0], True