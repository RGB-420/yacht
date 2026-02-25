from sqlalchemy import text

def upsert_owner(conn, name):
    insert_query = text("""
        INSERT INTO yacht_db.owners (name)
        VALUES (:name)
                        
        ON CONFLICT (name)
        DO NOTHING
                        
        RETURNING id_owner;
    """)

    result = conn.execute(insert_query, {"name": name}).fetchone()

    if result:
        return result[0], True
    
    select_query = text("""
        SELECT id_owner
        FROM yacht_db.owners
        WHERE name = :name
    """)

    existing = conn.execute(select_query, {"name": name}).fetchone()

    return existing[0], False