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
        SELECT c.id_club, c.name, c.short_name, c.estimated_numbers, l.city, l.region, l.country
        FROM yacht_db.boat_clubs bc
                 
        JOIN yacht_db.clubs c
            ON bc.id_club = c.id_club
        LEFT JOIN yacht_db.locations l
            ON c.id_location = l.id_location
                 
        WHERE bc.id_boat = :boat_id
        ORDER BY c.name
    """)

    result = conn.execute(query, {"boat_id": boat_id})

    return rows_to_dict(result)

def get_club_boats(conn, club_id):
    query = text("""
        SELECT b.id_boat, b.name, b.boat_identifier, bc.id_class, bc.name AS class_name
        FROM yacht_db.boat_clubs bclu
        
        JOIN yacht_db.boats b
            ON bclu.id_boat = b.id_boat
        LEFT JOIN yacht_db.boat_type bt
            ON b.id_type = bt.id_type
        LEFT JOIN yacht_db.boat_classes bc
            ON bt.id_class = bc.id_class

        WHERE bclu.id_club = :club_id

        ORDER BY b.name 
    """)

    result = conn.execute(query, {"club_id": club_id})

    return rows_to_dict(result)
