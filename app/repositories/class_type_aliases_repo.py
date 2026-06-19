from sqlalchemy import text

def create_pending_class_type_alias(conn, raw_class, raw_type, normalized_class, normalized_type):
    query = text("""
        INSERT INTO yacht_norm.class_type_aliases(raw_class, raw_type, normalized_class, normalized_type, status)
        VALUES (:raw_class, :raw_type, :normalized_class, :normalized_type, 'pending')
                 
        ON CONFLICT (raw_class, raw_type)
        DO NOTHING
    """)

    conn.execute(query, {"raw_class": raw_class, "raw_type": raw_type, "normalized_class": normalized_class, "normalized_type": normalized_type})

def bulk_upsert_class_type_aliases(conn, rows):
    query = text("""
        INSERT INTO yacht_norm.class_type_aliases (raw_class, raw_type, normalized_class, normalized_type, status, confidence)
        VALUES (:raw_class, :raw_type, :normalized_class, :normalized_type, :status, :confidence)
            
        ON CONFLICT (raw_class, raw_type)
        DO UPDATE SET 
            normalized_class = EXCLUDED.normalized_class,
            normalized_type = EXCLUDED.normalized_type,
            status = EXCLUDED.status,
            confidence = EXCLUDED.confidence
    """)

    conn.execute(query, rows)

def load_class_type_alias_cache(conn):
    query = text("""
        SELECT cta.id_alias, cta.raw_class, cta.raw_type, cta.normalized_class, cta.normalized_type, cta.status, cta.confidence, ct.canonical_class, ct.canonical_type
        FROM yacht_norm.class_type_aliases cta
        
        LEFT JOIN yacht_norm.class_type_alias_relations ctar
            ON ctar.id_alias = cta.id_alias
        
        LEFT JOIN yacht_norm.class_types ct
            ON ct.id_class_type = ctar.id_class_type
    """)

    rows = conn.execute(query).mappings().all()

    raw_cache = {}
    normalized_cache = {}

    for row in rows:
        row_dict = dict(row)

        raw_key = (str(row["raw_class"]).upper() if row["raw_class"] else None,
                   str(row["raw_type"]).upper() if row["raw_type"] else None)

        normalized_key = (str(row["normalized_class"]).upper() if row["normalized_class"] else None,
                          str(row["normalized_type"]).upper() if row["normalized_type"] else None)
        
        raw_cache[raw_key] = row_dict
        normalized_cache[normalized_key] = row_dict

    return raw_cache, normalized_cache

def get_all_class_type_mappings(conn):
    query = text("""
        SELECT cta.raw_class, cta.raw_type, cta.normalized_class, cta.normalized_type, cta.status, cta.confidence, cta.notes, ct.canonical_class, ct.canonical_type
        FROM yacht_norm.class_type_aliases cta
            
        LEFT JOIN yacht_norm.class_type_aliases ctar
            ON ctar.id_alias = cta.id_alias
                 
        LEFT JOIN yacht_norm.class_types ct
            ON ct.id_class_type = ctar.id_class_type
                 
        ORDER BY cta.raw_class, cta.raw_type
    """)

    result = conn.execute(query)

    return [dict(row._mapping) for row in result]
