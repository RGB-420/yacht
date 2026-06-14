from sqlalchemy import text

def load_club_alias_realtions_cache(conn):
    query = text("""
        SELECT id_alias, id_club
        FROM yacht_norm.club_alias_relations
    """)

    result = conn.execute(query)

    return {
        (row.id_alias, row.id_club)
        for row in result
    }

def bulk_insert_club_alias_relations(conn, rows):
    query = text("""
        INSERT INTO yacht_norm.club_alias_relations (id_alias, id_club)
        VALUES (:id_alias, :id_club)
                 
        ON CONFLICT (id_alias, id_club)
        DO NOTHING
    """)

    conn.execute(query, rows)

def delete_club_alias_relations(conn, id_alias):
    query = text("""
        DELETE FROM yacht_norm.club_alias_relations
        WHERE id_alias = :id_alias
    """)

    conn.execute(query, {"id_alias": id_alias})
    