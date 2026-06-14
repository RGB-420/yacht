from sqlalchemy import text

from app.services.mappings.club_alias_utils import group_club_alias_cache, group_club_mappings


def find_club_alias_by_raw_name(conn, raw_name):
    query = text("""
        SELECT ca.id_alias, ca.raw_name, ca.normalized_name, ca.status, ca.confidence, c.canonical_name
        FROM yacht_norm.club_aliases ca
                 
        LEFT JOIN yacht_norm.club_alias_relations car
            ON car.id_alias = ca.id_alias

        LEFT JOIN yacht_norm.clubs c
            ON car.id_club = c.id_club
                 
        WHERE UPPER(ca.raw_name) = UPPER(:raw_name)
    """)

    rows = conn.execute(query, {"raw_name": raw_name}).mappings().all()

    rows = group_club_alias_cache(rows)

    if not rows:
        return None

    return rows[0]


def find_club_alias_by_normalized_name(conn, normalized_name):
    query = text("""
        SELECT ca.id_alias, ca.raw_name, ca.normalized_name, ca.status, ca.confidence, c.canonical_name
        FROM yacht_norm.club_aliases ca
                 
        LEFT JOIN yacht_norm.club_alias_relations car
            ON car.id_alias = ca.id_alias
                 
        LEFT JOIN yacht_norm.clubs c
            ON car.id_club = c.id_club
        
        WHERE UPPER(ca.normalized_name) = UPPER(:normalized_name)
    """)

    rows = conn.execute(query, {"normalized_name": normalized_name}).mappings().all()

    rows = group_club_alias_cache(rows)

    if not rows:
        return None

    return rows[0]


def create_pending_club_alias(conn, raw_name, normalized_name):
    query = text("""
        INSERT INTO yacht_norm.club_aliases (raw_name, normalized_name, status)
        VALUES (:raw_name, :normalized_name, 'pending')
        ON CONFLICT DO NOTHING
    """)

    conn.execute(query, {"raw_name": raw_name, "normalized_name": normalized_name})
    
def upsert_club_alias(conn, raw_name, normalized_name, id_club, status, confidence):
    query = text("""
        INSERT INTO yacht_norm.club_aliases (raw_name, normalized_name, id_club, status, confidence)
        VALUES (:raw_name, :normalized_name, :id_club, :status, :confidence)
        
        ON CONFLICT (raw_name)
        
        DO UPDATE SET
            normalized_name = EXCLUDED.normalized_name,
            id_club = EXCLUDED.id_club,
            status = EXCLUDED.status,
            confidence = EXCLUDED.confidence
    """)

    conn.execute(query, {"raw_name": raw_name, "normalized_name": normalized_name, "id_club": id_club, "status": status, "confidence": confidence})


def bulk_upsert_club_aliases(conn, rows):
    query = text("""
        INSERT INTO yacht_norm.club_aliases (raw_name, normalized_name, status, confidence)
        VALUES (:raw_name, :normalized_name, :status, :confidence)
                 
        ON CONFLICT (raw_name)
        DO UPDATE SET
            normalized_name = EXCLUDED.normalized_name,
            status = EXCLUDED.status,
            confidence = EXCLUDED.confidence
    """)

    conn.execute(query, rows)


def get_pending_club_aliases(conn):
    query = text("""
        SELECT raw_name, normalized_name, COUNT(*) AS occurrences
        FROM yacht_norm.club_aliases
        WHERE status = 'pending'
        GROUP BY raw_name, normalized_name
        ORDER BY occurrences DESC
    """)

    result = conn.execute(query)

    return [dict(row._mapping) for row in result]

def get_resolved_club_aliases(conn):
    query = text("""
        SELECT ca.raw_name, ca.normalized_name, c.canonical_name
        FROM yacht_norm.club_aliases ca
        
        JOIN yacht_norm.club_alias_relations car
            ON car.id_alias = ca.id_alias

        JOIN yacht_norm.clubs c
            ON c.id_club=car.id_club
                 
        WHERE status = 'resolved'
        AND canonical_name IS NOT NULL
    """)

    result = conn.execute(query)

    return [dict(row._mapping) for row in result]

def load_club_alias_cache(conn):
    query = text("""
        SELECT ca.id_alias, ca.raw_name, ca.normalized_name, ca.status, ca.confidence, c.canonical_name
        FROM yacht_norm.club_aliases ca


        LEFT JOIN yacht_norm.club_alias_relations car
            ON car.id_alias = ca.id_alias
        LEFT JOIN yacht_norm.clubs c
            ON car.id_club = c.id_club
    """)

    rows = conn.execute(query).mappings().all()

    rows = group_club_alias_cache(rows)

    raw_cache = {}
    normalized_cache = {}

    for row in rows:
        row_dict = dict(row)

        raw_name = row["raw_name"]
        normalized_name = row["normalized_name"]

        if raw_name:
            raw_cache[str(raw_name).upper()] = row_dict
        
        if normalized_name:
            normalized_cache[str(normalized_name).upper()] = row_dict

    return raw_cache, normalized_cache

def get_all_club_mappings(conn):
    query = text("""
        SELECT ca.id_alias, ca.raw_name, ca.normalized_name, ca.status, ca.confidence, ca.alias_type, ca.notes, c.canonical_name, c.country, c.website, c.entity_type

        FROM yacht_norm.club_aliases ca

        LEFT JOIN yacht_norm.club_alias_relations car
            ON car.id_alias = ca.id_alias

        LEFT JOIN yacht_norm.clubs c
            ON c.id_club = car.id_club
        
        ORDER BY ca.raw_name
    """)

    rows = conn.execute(query).mappings().all()

    rows= group_club_mappings(rows)

    return rows
