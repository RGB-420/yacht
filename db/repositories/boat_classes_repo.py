from sqlalchemy import text

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
                 
        RETURNING id_class, (cmax = 0) AS inserted;
    """)

    result = conn.execute(query, {"name": name, "manufacturer": manufacturer, "category": category, "rating_rule": rating_rule, "start_year": start_year, "crew_min": crew_min, "crew_max": crew_max, "length_m":length_m}).fetchone()

    return result[0], result[1]
