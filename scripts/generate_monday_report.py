import pandas as pd
from datetime import datetime, timedelta

from db.connection import get_engine
from app.repositories.report_repo import get_monday_report

from app.core.config import DATA_REPORT


def main():
    engine = get_engine()

    clubs = ["RTYC", "ROYAL THAMES YC", "ROYAL THAMES YACHT CLUB"]
    regattas = [
        "RORC Easter Regatta - 2026"
    ]

    all_rows = []

    with engine.connect() as conn:
        for regatta in regattas:
            regatta_name, year = [x.strip() for x in regatta.split("-")]

            rows = get_monday_report(conn, clubs, regatta_name, year)

            all_rows.extend(rows)

    columns = ["regatta", "owner", "boat", "results_link"]
    df = pd.DataFrame(all_rows, columns=columns)

    monday = get_monday()

    output_path = DATA_REPORT / f"monday_week_report_{monday}.csv"
    
    df.to_csv(output_path, index=False)

    print("Monday report generado correctamente")

def get_monday():
    today = datetime.today()

    monday = today - timedelta(days=today.weekday())

    return monday.strftime('%Y-%m-%d')

if __name__ == "__main__":
    main()