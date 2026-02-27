from sqlalchemy import text

def insert_boat_editions(conn, boat_id, edition_id):
    query = text("""
        INSERT INTO yacht_db.boat_editions (id_boat, id_edition)
        VALUES (:boat_id, :edition_id)
                 
        ON CONFLICT (id_boat, id_edition)
        DO NOTHING;
    """)

    conn.execute(query, {"boat_id": boat_id, "edition_id": edition_id})