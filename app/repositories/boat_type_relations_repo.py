from sqlalchemy import text

from app.core.db import rows_to_dict 

def insert_boat_type_relation(conn, boat_id, type_id):
    query = text("""
        INSERT INTO yacht_db.boat_type_relations (id_boat, id_type)
        VALUES (:boat_id, :type_id)
                 
        ON CONFLICT (id_boat, id_type)
        DO NOTHING  
    """)

    conn.execute(query, {"boat_id": boat_id, "type_id": type_id})

def load_boat_type_rel_cache(conn):
    query = text("""
        SELECT id_boat, id_type
        FROM yacht_db.boat_type_relations
    """)

    rows = conn.execute(query).fetchall()

    return {(row.id_boat, row.id_type) for row in rows}

def get_boat_types(conn, boat_id):
    query = text("""
        SELECT bt.id_type, bt.name, bt.id_class
        FROM yacht_db.boat_type_relations btr
                 
        JOIN yacht_db.boat_type bt
            ON btr.id_type = bt.id_type
                 
        WHERE btr.id_boat = :boat_id
        
        ORDER BY bt.name
    """)

    result = conn.execute(query, {"boat_id": boat_id})

    return rows_to_dict(result)