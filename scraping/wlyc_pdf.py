import camelot
import pandas as pd
import re
from pathlib import Path

def scrape(route):
    route = Path(route)

    tables = camelot.read_pdf(
        str(route),
        pages="2-3",
        flavor="stream"
    )

    rows = []

    for table in tables:
        df = table.df

        for _, row in df.iterrows():
            text = " ".join(str(x) for x in row if x.strip() != "")

            if "Team Name" in text or "Posn" in text:
                continue

            match = re.search(r"\b(FF|GP|EN)\b\s+([A-Z0-9 ]+)", text)
            if not match:
                continue

            boat_class = match.group(1)
            sail_no = match.group(2).strip().split()[0]

            team_name = text.split(boat_class)[0]

            team_name = re.sub(r"^\d+\s*", "", team_name).strip()

            rows.append({
                "Team Name": team_name,
                "Sail No": sail_no
            })

    result = pd.DataFrame(rows)

    result = result.drop_duplicates()

    return result
