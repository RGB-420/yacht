from sqlalchemy import text, bindparam

def get_monday_report(conn, clubs, regatta, year):
    query = text("""
        SELECT DISTINCT
            r.name AS regatta,
            o.name AS owner,
            b.name AS boat,
            rl.url AS results_link

        FROM yacht_db.boats b

        JOIN yacht_db.boats_owner bo 
            ON bo.id_boat = b.id_boat
        JOIN yacht_db.owners o 
            ON o.id_owner = bo.id_owner

        JOIN yacht_db.boat_clubs bc 
            ON bc.id_boat = b.id_boat
        JOIN yacht_db.clubs c 
            ON c.id_club = bc.id_club

        JOIN yacht_db.boat_editions be 
            ON be.id_boat = b.id_boat
        JOIN yacht_db.regatta_editions re 
            ON re.id_edition = be.id_edition
        JOIN yacht_db.regattas r 
            ON r.id_regatta = re.id_regatta

        LEFT JOIN yacht_db.regatta_links rl
            ON re.id_edition = rl.id_edition

        WHERE c.name IN :clubs
        AND r.name = :regattas
        AND re.year = :year
    """)

    query = query.bindparams(bindparam("clubs", expanding=True))

    result = conn.execute(query, {"clubs": clubs, "regattas": regatta, "year": year}).fetchall()

    return result 