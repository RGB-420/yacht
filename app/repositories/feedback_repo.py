from sqlalchemy import text

def create_feedback(conn, entity_type, entity_id, type_, message, page, link=None):
    query = text("""
        INSERT INTO yacht_db.feedback (entity_type, entity_id, type, message, page, link)
            VALUES (:entity_type, :entity_id, :type, :message, :page, :link)
                 
        RETURNING id_feedback
    """)

    result = conn.execute(query, {"entity_type": entity_type, "entity_id": entity_id, "type": type_, "message": message, "page": page, "link": link}).fetchone()

    return result[0]

