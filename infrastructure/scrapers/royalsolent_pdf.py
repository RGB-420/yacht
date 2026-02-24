import camelot
import pandas as pd
from pathlib import Path

def scrape(route):
    route = Path(route)
    
    tables = camelot.read_pdf(str(route), pages="all", flavor="stream")

    data = []
    current_class = None

    for table in tables:
        df = table.df

        for i, row in df.iterrows():
            cell = row[0].strip()

            if cell.lower().startswith("class"):
                current_class = cell
                continue

            if cell.lower() in ["name", "boat name", ""]:
                continue

            if len(row) >= 5 and current_class is not None:
                data.append({
                    "class": current_class,
                    "name": row[0],
                    "type": row[2],
                    "sail_no": row[3],
                    "owner": row[4]
                })

    final_df = pd.DataFrame(data)

    return final_df
