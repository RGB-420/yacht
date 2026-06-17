from pathlib import Path

import pandas as pd

from db.connection import get_engine

EXPORT_DIR = Path("data/exports")
EXPORT_DIR.mkdir(exist_ok=True)

RTYC_DB_CLUB_ID = 39
RTYC_NORM_CLUB_ID = 319

def export_rtyc():
    engine = get_engine()

    print("Exporting RTYC data...")

    query = """
    SELECT DISTINCT
        b.id_boat,
        b.name AS boat_name,
        b.boat_identifier,

        o.id_owner,
        o.name AS owner_name,

        c.id_club,
        c.name AS source_club_name

    FROM yacht_db.boats b

    JOIN yacht_db.boat_clubs bc
        ON b.id_boat = bc.id_boat

    JOIN yacht_db.clubs c
        ON bc.id_club = c.id_club

    LEFT JOIN yacht_db.boats_owner bo
        ON b.id_boat = bo.id_boat

    LEFT JOIN yacht_db.owners o
        ON bo.id_owner = o.id_owner

    WHERE bc.id_club = %(club_id)s

    ORDER BY boat_name
    """

    rtyc_df = pd.read_sql(
        query,
        engine,
        params={"club_id": RTYC_DB_CLUB_ID},
    )

    output_file = EXPORT_DIR / "rtyc_export.csv"

    rtyc_df.to_csv(output_file, index=False)

    print(
        f"✓ RTYC export: {len(rtyc_df)} rows"
    )

    evidence_query = """
    SELECT
        a.raw_name,
        a.normalized_name,
        a.status,
        a.confidence,
        c.canonical_name

    FROM yacht_norm.club_aliases a

    JOIN yacht_norm.club_alias_relations r
        ON a.id_alias = r.id_alias

    JOIN yacht_norm.clubs c
        ON r.id_club = c.id_club

    WHERE r.id_club = %(club_id)s

    ORDER BY a.raw_name
    """

    evidence_df = pd.read_sql(
        evidence_query,
        engine,
        params={"club_id": RTYC_NORM_CLUB_ID},
    )

    evidence_file = (
        EXPORT_DIR / "rtyc_matching_evidence.csv"
    )

    evidence_df.to_csv(
        evidence_file,
        index=False,
    )

    print(
        f"✓ RTYC evidence: {len(evidence_df)} rows"
    )

    print("\nDone.")

if __name__ == "__main__":
    export_rtyc()
