from sqlalchemy import text

def get_boats_quality_metrics(conn):
    total_boats = conn.execute(text("""
        SELECT COUNT(*)
        FROM yacht_db.boats
    """)).scalar()

    boats_with_type = conn.execute(text("""
        SELECT COUNT(DISTINCT id_boat)
        FROM yacht_db.boat_type_relations
    """)).scalar()

    boats_with_owner = conn.execute(text("""
        SELECT COUNT(DISTINCT id_boat)
        FROM yacht_db.boats_owner
    """)).scalar()

    boats_with_club = conn.execute(text("""
        SELECT COUNT(DISTINCT id_boat)
        FROM yacht_db.boat_clubs
    """)).scalar()

    boats_with_class = conn.execute(text("""
        SELECT COUNT(DISTINCT btr.id_boat)
        FROM yacht_db.boat_type_relations btr
                                    
        JOIN yacht_db.boat_type bt
            ON bt.id_type = btr.id_type
                                         
        WHERE bt.id_class IS NOT NULL
    """)).scalar()

    return {
        "total_boats": total_boats,

        "boats_with_type": boats_with_type,
        "boats_without_type": total_boats - boats_with_type,

        "boats_with_class": boats_with_class,
        "boats_without_class": total_boats - boats_with_class,

        "boats_with_owner": boats_with_owner,
        "boats_without_owner": total_boats - boats_with_owner,

        "boats_with_club": boats_with_club,
        "boats_without_club": total_boats - boats_with_club
    }

def get_clubs_quality_metrics(conn):
    query = text("""
        SELECT COUNT(*)
        FROM yacht_db.clubs
    """)

    result = conn.execute(query)

    return {"total_clubs": result.scalar()}

def get_owners_quality_metrics(conn):
    query = text("""
        SELECT COUNT(*)
        FROM yacht_db.owners
    """)

    result = conn.execute(query)

    return {"total_owners": result.scalar()}

def get_regattas_quality_metrics(conn):
    query = text("""
        SELECT COUNT(*)
    """)