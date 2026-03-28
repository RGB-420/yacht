from sqlalchemy import text

from app.core.db import rows_to_dict

def insert_boat_owner(conn, boat_id, owner_id):
    query = text("""
        INSERT INTO yacht_db.boats_owner (id_boat, id_owner)
        VALUES (:boat_id, :owner_id)
                 
        ON CONFLICT (id_boat, id_owner) DO NOTHING;
    """)

    conn.execute(query, {"boat_id": boat_id, "owner_id":owner_id})

def get_boat_owners(conn, boat_id):
    query = text("""
        SELECT o.id_owner, o.name
        FROM yacht_db.boats_owner bo
        JOIN yacht_db.owners o
            ON bo.id_owner = o.id_owner
        
        WHERE bo.id_boat = :boat_id
        ORDER BY o.name
    """)

    result = conn.execute(query, {"boat_id": boat_id})

    return rows_to_dict(result)
