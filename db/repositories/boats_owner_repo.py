from sqlalchemy import text

def insert_boat_owner(conn, boat_id, owner_id):
    query = text("""
        INSERT INTO yacht_db.boats_owner (id_boat, id_owner)
        VALUES (:boat_id, :owner_id)
                 
        ON CONFLICT (id_boat, id_owner) DO NOTHING;
    """)

    conn.execute(query, {"boat_id": boat_id, "owner_id":owner_id})