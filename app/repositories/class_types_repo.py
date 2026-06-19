from sqlalchemy import text

def find_class_type_by_canonical(conn, canonical_class, canonical_type):
    query = text("""
        SELECT id_class_type, canonical_class, canonical_type
        FROM yacht_norm.class_types
        WHERE UPPER(canonical_class) = UPPER(:canonical_class)
            AND UPPER(canonical_type) = UPPER(:canonical_type)
    """)

    result = conn.execute(query, {"canonical_class": canonical_class, "canonical_type": canonical_type}).mappings().first()

    return result

def load_class_type_cache(conn):
    query = text("""
        SELECT id_class_type, canonical_class, canonical_type
        FROM yacht_norm.class_types
    """)

    rows = conn.execute(query).mappings().all()

    return {
        (str(row["canonical_class"]).upper() if row["canonical_class"] else None, str(row["canonical_type"]).upper() if row["canonical_type"] else None): row["id_class_type"]
        for row in rows
        if row["canonical_class"] or row["canonical_type"]
    }

def bulk_upsert_class_types(conn, rows):
    query = text("""
        INSERT INTO yacht_norm.class_types (canonical_class, canonical_type)
        VALUES (:canonical_class, :canonical_type)
        
        ON CONFLICT (canonical_class, canonical_type)
        DO NOTHING
    """)

    conn.execute(query, rows)
    