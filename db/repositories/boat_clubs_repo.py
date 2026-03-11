from sqlalchemy import text

from utils.db_utils import rows_to_dict

def insert_boat_club(conn, boat_id, club_id):
    query = text("""
        INSERT INTO yacht_db.boat_clubs (id_boat, id_club)
        VALUES (:boat_id, :club_id)
                 
        ON CONFLICT (id_boat, id_club)
        DO NOTHING;
    """)

    conn.execute(query, {"boat_id": boat_id, "club_id": club_id})
    
def get_boat_clubs(conn, boat_id):
    query = text("""
        SELECT c.id_club, c.name, c.short_name
        FROM yacht_db.boat_clubs bc
        JOIN yacht_db.clubs c
            ON bc.id_club = c.id_club
        WHERE bc.id_boat = :boat_id
        ORDER BY c.name
    """)

    result = conn.execute(query, {"boat_id": boat_id})

    return rows_to_dict(result)
