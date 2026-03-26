from sqlalchemy import text

from utils.db_utils import row_to_dict, rows_to_dict

def upsert_club(conn, name, short_name=None, estimated_numbers=None, location_id=None):
    query = text("""
        INSERT INTO yacht_db.clubs (name, short_name, estimated_numbers, id_location)
        VALUES (:name, :short_name, :estimated_numbers, :location_id)
                 
        ON CONFLICT (name) DO UPDATE SET
            short_name = COALESCE(EXCLUDED.short_name, yacht_db.clubs.short_name),
            estimated_numbers = COALESCE(EXCLUDED.estimated_numbers, yacht_db.clubs.estimated_numbers),
            id_location = COALESCE(EXCLUDED.id_location, yacht_db.clubs.id_location)
                 
        RETURNING id_club, (xmax=0) AS inserted
    """)

    result = conn.execute(query, {"name": name, "short_name": short_name, "estimated_numbers": estimated_numbers, "location_id": location_id}).fetchone()

    return result[0], result[1]

def get_all_clubs_with_location(conn):
    query = text("""
        SELECT c.name, c.short_name, c.estimated_numbers, l.city, l.region, l.country
        FROM yacht_db.clubs c

        LEFT JOIN yacht_db.locations l 
            ON c.id_location = l.id_location
    """)
    
    result = conn.execute(query).fetchall()

    return result

def get_clubs(conn):
    query = text("""    
        SELECT c.id_club, c.name, c.short_name, c.estimated_numbers, l.city, l.region, l.country
        FROM yacht_db.clubs c
        
        LEFT JOIN yacht_db.locations l
            ON c.id_location = l.id_location
                 
        ORDER BY c.name
    """)

    result = conn.execute(query)

    return rows_to_dict(result)

def get_club_by_id(conn, club_id):
    query = text("""
        SELECT c.id_club, c.name, c.short_name, c.estimated_numbers, l.city, l.region, l.country,
            COUNT(DISTINCT bc.id_boat) AS number_of_boats,
            COUNT(DISTINCT r.id_regatta) AS number_of_regattas
        FROM yacht_db.clubs c
            
        LEFT JOIN yacht_db.locations l
            ON c.id_location = l.id_location
        LEFT JOIN yacht_db.boat_clubs bc    
            ON c.id_club = bc.id_club
        LEFT JOIN yacht_db.regattas r
            ON c.id_club = r.id_club
        
        WHERE c.id_club = :club_id
            
        GROUP BY c.id_club, c.name, c.short_name, c.estimated_numbers, l.city, l.region, l.country
    """)

    result = conn.execute(query, {"club_id": club_id}).fetchone()

    return row_to_dict(result)

def get_clubs_scorecard(conn, week_ago):
    query = text("""
                SELECT 
                    COUNT(*) as total_active,
                    SUM(CASE 
                        WHEN created_at >= :week_ago THEN 1 
                        ELSE 0 
                    END) as new_sourced
                FROM yacht_db.clubs
            """)
    
    result = conn.execute(query, {"week_ago": week_ago}).fetchone()

    return {"total_active": result[0], "new_sourced":result[1]}
