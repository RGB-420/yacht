from sqlalchemy import text

def create_feedback(conn, entity_type, entity_id, type_, message, page):
    query = text("""
        INSERT INTO yacht_db.feedback (entity_type, entity_id, type, message, page)
            VALUES (:entity_type, :entity_id, :type, :message, :page)
                 
        RETURNING id_feedback
    """)

    result = conn.execute(query, {"entity_type": entity_type, "entity_id": entity_id, "type": type_, "message": message, "page": page}).fetchone()

    return result[0]

