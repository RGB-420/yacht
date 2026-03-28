from sqlalchemy import text

from app.core.db import rows_to_dict

def upsert_regatta_link(conn, edition_id, url):
    query = text("""
        INSERT INTO yacht_db.regatta_links (id_edition, url)
            VALUES (:edition_id, :url)
                 
        ON CONFLICT (id_edition, url)
        DO NOTHING
                 
        RETURNING id_link;
    """)

    result = conn.execute(query, {"edition_id": edition_id, "url": url})

    return bool(result)

def get_regatta_links(conn, regatta_id):
    query = text("""
        SELECT rl.id_link, rl.url, re.year
        FROM yacht_db.regatta_links rl
        JOIN yacht_db.regatta_editions re ON rl.id_edition = re.id_edition
        WHERE re.id_regatta = :regatta_id
        ORDER BY re.year DESC
    """)

    result = conn.execute(query, {"regatta_id": regatta_id})

    return rows_to_dict(result)