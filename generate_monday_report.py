import pandas as pd
from datetime import datetime, timedelta

from db.connection import get_engine
from db.repositories.report_repo import get_monday_report


def main():
    engine = get_engine()

    clubs = ["RTYC", "ROYAL THAMES YC", "ROYAL THAMES YACHT CLUB"]
    regattas = [
        "British Classic Week",
        "Cowes Week"
    ]

    with engine.connect() as conn:
        rows = get_monday_report(conn, clubs, regattas)

    columns = ["regatta", "owner", "boat", "results_link"]
    df = pd.DataFrame(rows, columns=columns)

    monday = get_monday()

    df.to_csv(f"data/report/monday_report_week_{monday}.csv", index=False)

    print("Monday report generado correctamente")

def get_monday():
    today = datetime.today()

    monday = today - timedelta(days=today.weekday())

    return monday.strftime('%Y-%m-%d')

if __name__ == "__main__":
    main()