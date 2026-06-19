from sqlalchemy import text

def load_class_type_alias_relations_cache(conn):
    query = text("""
        SELECT id_alias, id_class_type
        FROM yacht_norm.class_type_alias_relations
    """)

    result = conn.execute(query)

    return {
        (row.id_alias, row.id_class_type)
        for row in result
    }

def bulk_insert_class_type_alias_relations(conn, rows):
    query = text("""
        INSERT INTO yacht_norm.class_type_alias_relations (id_alias, id_class_type)
        VALUES (:id_alias, :id_class_type)
        
        ON CONFLICT (id_alias, id_class_type)
        DO NOTHING
    """)

    conn.execute(query, rows)

def delete_class_type_alias_relations(conn, id_alias):
    query = text("""
        DELETE FROM yacht_norm.class_type_alias_relations
        WHERE id_alias = :id_alias
    """)

    conn.execute(query, {"id_alias": id_alias})