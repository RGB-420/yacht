from sqlalchemy import text

from app.core.db import rows_to_dict

def upsert_regatta_schedule(conn, edition_id):
    query = text("""
        INSERT INTO yacht_db.regatta_schedule (id_edition)
        VALUES (:edition_id)
        
        ON CONFLICT (id_edition)
        DO NOTHING
    """)

    result = conn.execute(query, {"edition_id": edition_id})

    return result

def upsert_regatta_schedule_dates(conn, edition_id, start_date, end_date):
    query = text("""
        INSERT INTO yacht_db.regatta_schedule (id_edition, start_date, end_date)
        VALUES (:edition_id, :start_date, :end_date)
        
        ON CONFLICT (id_edition)
        DO UPDATE SET
            start_date = EXCLUDED.start_date,
            end_date = EXCLUDED.end_date
    """)

    result = conn.execute(query, {"edition_id": edition_id, "start_date": start_date, "end_date": end_date})

    return result

def get_all_schedule_with_regatta(conn):
    query = text("""
        SELECT r.name AS regatta_name,
               e.year,
               rs.start_date,
               rs.end_date
        FROM yacht_db.regatta_schedule rs
        JOIN yacht_db.regatta_editions e 
            ON e.id_edition = rs.id_edition
        JOIN yacht_db.regattas r 
            ON r.id_regatta = e.id_regatta
    """)

    result = conn.execute(query).fetchall()

    return result

def get_schedule_with_dates(conn):
    query = text("""
        SELECT r.id_regatta, r.name AS regatta_name, e.id_edition, e.year, rs.start_date, rs.end_date
        FROM yacht_db.regatta_schedule rs
        JOIN yacht_db.regatta_editions e 
            ON e.id_edition = rs.id_edition
        JOIN yacht_db.regattas r 
            ON r.id_regatta = e.id_regatta

        WHERE rs.start_date IS NOT NULL
        
        ORDER BY rs.start_date ASC
    """)

    result = conn.execute(query)

    return rows_to_dict(result)