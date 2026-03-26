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

def get_owners_scorecard(conn, week_ago):
    query = text("""
                SELECT 
                    COUNT(*) as total_active,
                    SUM(CASE 
                        WHEN created_at >= :week_ago THEN 1 
                        ELSE 0 
                    END) as new_sourced
                FROM yacht_db.owners""")
    
    result = conn.execute(query, {"week_ago": week_ago}).fetchone()

    return {"total_active": result[0], "new_sourced": result[0]}
