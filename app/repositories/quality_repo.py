from sqlalchemy import text


def _coverage_metric(key, label, total, covered):
    covered = covered or 0
    total = total or 0
    missing = total - covered
    coverage_pct = round((covered / total) * 100, 2) if total else 0

    return {
        "key": key,
        "label": label,
        "total": total,
        "covered": covered,
        "missing": missing,
        "coverage_pct": coverage_pct,
    }


def _issue_group(key, label, total, samples):
    return {
        "key": key,
        "label": label,
        "total": total or 0,
        "samples": samples,
    }


def _boat_sample_select():
    return """
        SELECT
            b.id_boat,
            b.name,
            b.boat_identifier,
            ARRAY_REMOVE(ARRAY_AGG(DISTINCT bt.name), NULL) AS types,
            ARRAY_REMOVE(ARRAY_AGG(DISTINCT bc.name), NULL) AS classes,
            ARRAY_REMOVE(ARRAY_AGG(DISTINCT o.name), NULL) AS owners,
            ARRAY_REMOVE(ARRAY_AGG(DISTINCT c.name), NULL) AS clubs
        FROM yacht_db.boats b
        LEFT JOIN yacht_db.boat_type_relations btr
            ON btr.id_boat = b.id_boat
        LEFT JOIN yacht_db.boat_type bt
            ON bt.id_type = btr.id_type
        LEFT JOIN yacht_db.boat_classes bc
            ON bc.id_class = bt.id_class
        LEFT JOIN yacht_db.boats_owner bo
            ON bo.id_boat = b.id_boat
        LEFT JOIN yacht_db.owners o
            ON o.id_owner = bo.id_owner
        LEFT JOIN yacht_db.boat_clubs bclu
            ON bclu.id_boat = b.id_boat
        LEFT JOIN yacht_db.clubs c
            ON c.id_club = bclu.id_club
    """


BOAT_ISSUE_LABELS = {
    "missing_type": "Boats without type",
    "missing_class": "Boats without class",
    "missing_owner": "Boats without owner",
    "missing_club": "Boats without club",
    "multiple_types": "Boats with multiple types",
}


def get_boats_quality_metrics(conn):
    query = text("""
        SELECT
            COUNT(*) AS total_boats,
            COUNT(*) FILTER (
                WHERE NULLIF(BTRIM(b.boat_identifier), '') IS NOT NULL
            ) AS boats_with_identifier,
            COUNT(*) FILTER (
                WHERE EXISTS (
                    SELECT 1
                    FROM yacht_db.boat_type_relations btr
                    WHERE btr.id_boat = b.id_boat
                )
            ) AS boats_with_type,
            COUNT(*) FILTER (
                WHERE EXISTS (
                    SELECT 1
                    FROM yacht_db.boat_type_relations btr
                    JOIN yacht_db.boat_type bt
                        ON bt.id_type = btr.id_type
                    WHERE btr.id_boat = b.id_boat
                        AND bt.id_class IS NOT NULL
                )
            ) AS boats_with_class,
            COUNT(*) FILTER (
                WHERE EXISTS (
                    SELECT 1
                    FROM yacht_db.boats_owner bo
                    WHERE bo.id_boat = b.id_boat
                )
            ) AS boats_with_owner,
            COUNT(*) FILTER (
                WHERE EXISTS (
                    SELECT 1
                    FROM yacht_db.boat_clubs bc
                    WHERE bc.id_boat = b.id_boat
                )
            ) AS boats_with_club,
            COUNT(*) FILTER (
                WHERE EXISTS (
                    SELECT 1
                    FROM yacht_db.boat_editions be
                    WHERE be.id_boat = b.id_boat
                )
            ) AS boats_with_edition
        FROM yacht_db.boats b
    """)

    row = conn.execute(query).mappings().one()

    multiple_types_query = text("""
        SELECT COUNT(*)
        FROM (
            SELECT id_boat
            FROM yacht_db.boat_type_relations
            GROUP BY id_boat
            HAVING COUNT(DISTINCT id_type) > 1
        ) boats_with_multiple_types
    """)

    boats_with_multiple_types = conn.execute(multiple_types_query).scalar() or 0
    total_boats = row["total_boats"] or 0

    return {
        "total_boats": total_boats,
        "coverage": [
            _coverage_metric(
                "identifier",
                "Boat identifier",
                total_boats,
                row["boats_with_identifier"],
            ),
            _coverage_metric(
                "type",
                "Boat type",
                total_boats,
                row["boats_with_type"],
            ),
            _coverage_metric(
                "class",
                "Boat class",
                total_boats,
                row["boats_with_class"],
            ),
            _coverage_metric(
                "owner",
                "Owner",
                total_boats,
                row["boats_with_owner"],
            ),
            _coverage_metric(
                "club",
                "Club",
                total_boats,
                row["boats_with_club"],
            ),
            _coverage_metric(
                "edition",
                "Regatta edition",
                total_boats,
                row["boats_with_edition"],
            ),
        ],
        "boats_with_multiple_types": boats_with_multiple_types,
    }


def get_boats_quality_issues(conn, limit=10):
    missing_type_total = conn.execute(text("""
        SELECT COUNT(*)
        FROM yacht_db.boats b
        WHERE NOT EXISTS (
            SELECT 1
            FROM yacht_db.boat_type_relations btr
            WHERE btr.id_boat = b.id_boat
        )
    """)).scalar()

    missing_type_samples = conn.execute(text(_boat_sample_select() + """
        WHERE NOT EXISTS (
            SELECT 1
            FROM yacht_db.boat_type_relations btr
            WHERE btr.id_boat = b.id_boat
        )
        GROUP BY b.id_boat, b.name, b.boat_identifier
        ORDER BY b.name, b.boat_identifier
        LIMIT :limit
    """), {"limit": limit}).mappings().all()

    missing_class_total = conn.execute(text("""
        SELECT COUNT(*)
        FROM yacht_db.boats b
        WHERE NOT EXISTS (
            SELECT 1
            FROM yacht_db.boat_type_relations btr
            JOIN yacht_db.boat_type bt
                ON bt.id_type = btr.id_type
            WHERE btr.id_boat = b.id_boat
                AND bt.id_class IS NOT NULL
        )
    """)).scalar()

    missing_class_samples = conn.execute(text(_boat_sample_select() + """
        WHERE NOT EXISTS (
            SELECT 1
            FROM yacht_db.boat_type_relations btr
            JOIN yacht_db.boat_type bt
                ON bt.id_type = btr.id_type
            WHERE btr.id_boat = b.id_boat
                AND bt.id_class IS NOT NULL
        )
        GROUP BY b.id_boat, b.name, b.boat_identifier
        ORDER BY b.name, b.boat_identifier
        LIMIT :limit
    """), {"limit": limit}).mappings().all()

    missing_owner_total = conn.execute(text("""
        SELECT COUNT(*)
        FROM yacht_db.boats b
        WHERE NOT EXISTS (
            SELECT 1
            FROM yacht_db.boats_owner bo
            WHERE bo.id_boat = b.id_boat
        )
    """)).scalar()

    missing_owner_samples = conn.execute(text(_boat_sample_select() + """
        WHERE NOT EXISTS (
            SELECT 1
            FROM yacht_db.boats_owner bo
            WHERE bo.id_boat = b.id_boat
        )
        GROUP BY b.id_boat, b.name, b.boat_identifier
        ORDER BY b.name, b.boat_identifier
        LIMIT :limit
    """), {"limit": limit}).mappings().all()

    missing_club_total = conn.execute(text("""
        SELECT COUNT(*)
        FROM yacht_db.boats b
        WHERE NOT EXISTS (
            SELECT 1
            FROM yacht_db.boat_clubs bc
            WHERE bc.id_boat = b.id_boat
        )
    """)).scalar()

    missing_club_samples = conn.execute(text(_boat_sample_select() + """
        WHERE NOT EXISTS (
            SELECT 1
            FROM yacht_db.boat_clubs bc
            WHERE bc.id_boat = b.id_boat
        )
        GROUP BY b.id_boat, b.name, b.boat_identifier
        ORDER BY b.name, b.boat_identifier
        LIMIT :limit
    """), {"limit": limit}).mappings().all()

    multiple_types_total = conn.execute(text("""
        SELECT COUNT(*)
        FROM (
            SELECT id_boat
            FROM yacht_db.boat_type_relations
            GROUP BY id_boat
            HAVING COUNT(DISTINCT id_type) > 1
        ) boats_with_multiple_types
    """)).scalar()

    multiple_types_samples = conn.execute(text(_boat_sample_select() + """
        GROUP BY b.id_boat, b.name, b.boat_identifier
        HAVING COUNT(DISTINCT btr.id_type) > 1
        ORDER BY b.name, b.boat_identifier
        LIMIT :limit
    """), {"limit": limit}).mappings().all()

    return {
        "limit": limit,
        "issues": [
            _issue_group(
                "missing_type",
                "Boats without type",
                missing_type_total,
                missing_type_samples,
            ),
            _issue_group(
                "missing_class",
                "Boats without class",
                missing_class_total,
                missing_class_samples,
            ),
            _issue_group(
                "missing_owner",
                "Boats without owner",
                missing_owner_total,
                missing_owner_samples,
            ),
            _issue_group(
                "missing_club",
                "Boats without club",
                missing_club_total,
                missing_club_samples,
            ),
            _issue_group(
                "multiple_types",
                "Boats with multiple types",
                multiple_types_total,
                multiple_types_samples,
            ),
        ],
    }


def get_boats_quality_issue(conn, issue_key, limit=100, offset=0):
    if issue_key not in BOAT_ISSUE_LABELS:
        return None

    if issue_key == "missing_type":
        total_query = text("""
            SELECT COUNT(*)
            FROM yacht_db.boats b
            WHERE NOT EXISTS (
                SELECT 1
                FROM yacht_db.boat_type_relations btr
                WHERE btr.id_boat = b.id_boat
            )
        """)

        samples_query = text(_boat_sample_select() + """
            WHERE NOT EXISTS (
                SELECT 1
                FROM yacht_db.boat_type_relations btr
                WHERE btr.id_boat = b.id_boat
            )
            GROUP BY b.id_boat, b.name, b.boat_identifier
            ORDER BY b.name, b.boat_identifier
            LIMIT :limit
            OFFSET :offset
        """)

    elif issue_key == "missing_class":
        total_query = text("""
            SELECT COUNT(*)
            FROM yacht_db.boats b
            WHERE NOT EXISTS (
                SELECT 1
                FROM yacht_db.boat_type_relations btr
                JOIN yacht_db.boat_type bt
                    ON bt.id_type = btr.id_type
                WHERE btr.id_boat = b.id_boat
                    AND bt.id_class IS NOT NULL
            )
        """)

        samples_query = text(_boat_sample_select() + """
            WHERE NOT EXISTS (
                SELECT 1
                FROM yacht_db.boat_type_relations btr
                JOIN yacht_db.boat_type bt
                    ON bt.id_type = btr.id_type
                WHERE btr.id_boat = b.id_boat
                    AND bt.id_class IS NOT NULL
            )
            GROUP BY b.id_boat, b.name, b.boat_identifier
            ORDER BY b.name, b.boat_identifier
            LIMIT :limit
            OFFSET :offset
        """)

    elif issue_key == "missing_owner":
        total_query = text("""
            SELECT COUNT(*)
            FROM yacht_db.boats b
            WHERE NOT EXISTS (
                SELECT 1
                FROM yacht_db.boats_owner bo
                WHERE bo.id_boat = b.id_boat
            )
        """)

        samples_query = text(_boat_sample_select() + """
            WHERE NOT EXISTS (
                SELECT 1
                FROM yacht_db.boats_owner bo
                WHERE bo.id_boat = b.id_boat
            )
            GROUP BY b.id_boat, b.name, b.boat_identifier
            ORDER BY b.name, b.boat_identifier
            LIMIT :limit
            OFFSET :offset
        """)

    elif issue_key == "missing_club":
        total_query = text("""
            SELECT COUNT(*)
            FROM yacht_db.boats b
            WHERE NOT EXISTS (
                SELECT 1
                FROM yacht_db.boat_clubs bc
                WHERE bc.id_boat = b.id_boat
            )
        """)

        samples_query = text(_boat_sample_select() + """
            WHERE NOT EXISTS (
                SELECT 1
                FROM yacht_db.boat_clubs bc
                WHERE bc.id_boat = b.id_boat
            )
            GROUP BY b.id_boat, b.name, b.boat_identifier
            ORDER BY b.name, b.boat_identifier
            LIMIT :limit
            OFFSET :offset
        """)

    else:
        total_query = text("""
            SELECT COUNT(*)
            FROM (
                SELECT id_boat
                FROM yacht_db.boat_type_relations
                GROUP BY id_boat
                HAVING COUNT(DISTINCT id_type) > 1
            ) boats_with_multiple_types
        """)

        samples_query = text(_boat_sample_select() + """
            GROUP BY b.id_boat, b.name, b.boat_identifier
            HAVING COUNT(DISTINCT btr.id_type) > 1
            ORDER BY b.name, b.boat_identifier
            LIMIT :limit
            OFFSET :offset
        """)

    total = conn.execute(total_query).scalar() or 0
    samples = conn.execute(
        samples_query,
        {"limit": limit, "offset": offset}
    ).mappings().all()

    return {
        "key": issue_key,
        "label": BOAT_ISSUE_LABELS[issue_key],
        "total": total,
        "limit": limit,
        "offset": offset,
        "samples": samples,
    }
