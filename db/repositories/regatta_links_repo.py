from sqlalchemy import text

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