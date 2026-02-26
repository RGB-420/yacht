from sqlalchemy import text 

def upsert_edition(conn, regatta_id, year):
    insert_query = text("""
        INSERT INTO yacht_db.regatta_editions (id_regatta, year)
        VALUES (:regatta_id, :year)
        
        ON CONFLICT (year, id_regatta)       
        DO NOTHING
                 
        RETURNING id_edition
    """)

    result = conn.execute(insert_query, {"regatta_id": regatta_id, "year": year}).fetchone()

    if result:
        return result[0], True
    
    select_query = text("""
        SELECT id_edition
        FROM yacht_db.regatta_editions
            WHERE id_regatta = :regatta_id
                AND year = :year;
    """)

    existing = conn.execute(select_query, {"regatta_id": regatta_id, "year": year}).fetchone()

    return existing[0], False

def get_edition_id(conn, regatta_name, year):
    query = text("""
        SELECT e.id_edition FROM yacht_db.regatta_editions e
        JOIN yacht_db.regattas r ON r.id_regatta = e.id_regatta
            WHERE r.name = :regatta_name
                AND e.year = :year
    """)

    result = conn.execute(query, {"regatta_name": regatta_name, "year": year}).fetchone()

    return result[0] if result else None