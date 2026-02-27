from sqlalchemy import text

def insert_boat_club(conn, boat_id, club_id):
    query = text("""
        INSERT INTO yacht_db.boat_clubs (id_boat, id_club)
        VALUES (:boat_id, :club_id)
                 
        ON CONFLICT (id_boat, id_club)
        DO NOTHING;
    """)

    conn.execute(query, {"boat_id": boat_id, "club_id": club_id})
    