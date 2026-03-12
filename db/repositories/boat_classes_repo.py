from sqlalchemy import text

from utils.db_utils import row_to_dict, rows_to_dict

def upsert_boat_classes(conn, name, manufacturer=None, category=None, rating_rule=None, start_year=None, crew_min=None, crew_max=None, length_m=None):
    query = text("""
        INSERT INTO yacht_db.boat_classes (name, manufacturer, category, rating_rule, start_year, crew_min, crew_max, length_m)
        VALUES (:name, :manufacturer, :category, :rating_rule, :start_year, :crew_min, :crew_max, :length_m)
                 
        ON CONFLICT (name) DO UPDATE SET
            manufacturer = COALESCE(EXCLUDED.manufacturer, yacht_db.boat_classes.manufacturer),
            category = COALESCE(EXCLUDED.category, yacht_db.boat_classes.category),
            rating_rule = COALESCE(EXCLUDED.rating_rule, yacht_db.boat_classes.rating_rule),
            start_year = COALESCE(EXCLUDED.start_year, yacht_db.boat_classes.start_year),
            crew_min = COALESCE(EXCLUDED.crew_min, yacht_db.boat_classes.crew_min),
            crew_max = COALESCE(EXCLUDED.crew_max, yacht_db.boat_classes.crew_max),
            length_m = COALESCE(EXCLUDED.length_m, yacht_db.boat_classes.length_m)
                 
        RETURNING id_class, (xmax = 0) AS inserted;
    """)

    result = conn.execute(query, {"name": name, "manufacturer": manufacturer, "category": category, "rating_rule": rating_rule, "start_year": start_year, "crew_min": crew_min, "crew_max": crew_max, "length_m":length_m}).fetchone()

    return result[0], result[1]

def get_class_id(conn, name):
    query = text("""
        SELECT id_class FROM yacht_db.boat_classes
        WHERE name = :name
    """)

    result = conn.execute(query, {"name": name})

    return result[0] if result else None

def get_classes(conn):
    query = text("""
        SELECT bc.id_class, bc.name, bc.manufacturer, bc.category, bc.rating_rule, bc.start_year, bc.crew_min, bc.crew_max, bc.length_m,
            COUNT(b.id_boat) AS number_of_boats
        FROM yacht_db.boat_classes bc
        
        LEFT JOIN yacht_db.boat_type as bt
            ON bt.id_class = bc.id_class
        LEFT JOIN yacht_db.boats b
            ON b.id_type = bt.id_type

        GROUP BY bc.id_class, bc.name, bc.manufacturer, bc.category, bc.rating_rule, bc.start_year, bc.crew_min, bc.crew_max, bc.length_m

        ORDER BY name
    """)

    result = conn.execute(query)

    return rows_to_dict(result)

def get_class_by_id(conn, class_id):
    query = text("""
        SELECT bc.id_class, bc.name, bc.manufacturer, bc.category, bc.rating_rule, bc.start_year, bc.crew_min, bc.crew_max, bc.length_m,
            COUNT(b.id_boat) AS number_of_boats
        FROM yacht_db.boat_classes bc
        
        LEFT JOIN yacht_db.boat_type bt
            ON bt.id_class = bc.id_class
        LEFT JOIN yacht_db.boats b
            ON b.id_type = bt.id_type
                 
        WHERE bc.id_class = :class_id
                 
        GROUP BY bc.id_class, bc.name, bc.manufacturer, bc.category, bc.rating_rule, bc.start_year, bc.crew_min, bc.crew_max, bc.length_m
    """)

    result = conn.execute(query, {"class_id": class_id}).fetchone()

    return row_to_dict(result)
