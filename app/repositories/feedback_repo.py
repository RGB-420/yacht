from sqlalchemy import text
from app.core.db import rows_to_dict

def create_feedback(conn, entity_type, entity_id, type_, message, page, link=None):
    query = text("""
        INSERT INTO yacht_db.feedback (entity_type, entity_id, type, message, page, link)
            VALUES (:entity_type, :entity_id, :type, :message, :page, :link)
                 
        RETURNING id_feedback
    """)

    result = conn.execute(query, {"entity_type": entity_type, "entity_id": entity_id, "type": type_, "message": message, "page": page, "link": link}).fetchone()

    return result[0]

def get_feedback(conn):
    query = text("""
        SELECT * FROM yacht_db.feedback
        ORDER BY created_at DESC
    """)

    result = conn.execute(query)

    return rows_to_dict(result)

def update_feedback_status(conn, feedback_id, status):
    query = text("""
        UPDATE yacht_db.feedback
        SET status = :status
        WHERE id_feedback = :feedback_id
    """)

    conn.execute(query, {"status": status, "feedback_id": feedback_id})
    