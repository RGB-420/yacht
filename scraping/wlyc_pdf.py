import camelot
import pandas as pd
import re
from pathlib import Path

from app.core.base_scraper import BaseScraper


class WLYCPDFScraper(BaseScraper):

    def __init__(self):
        super().__init__("wlyc_pdf")


    def scrape(self, route):
        route = Path(route)

        self.logger.info(f"[STEP] Processing PDF: {route}")

        try:
            tables = camelot.read_pdf(
                str(route),
                pages="2-3",
                flavor="stream"
            )

            self.logger.info(f"[INFO] Tables detected: {len(tables)}")

        except Exception as e:
            self.logger.error(f"[FAIL] Error reading PDF: {e}", exc_info=True)
            return None

        rows = []

        for table_idx, table in enumerate(tables):
            try:
                df = table.df

                self.logger.info(f"[STEP] Processing table {table_idx} ({len(df)} rows)")

                for _, row in df.iterrows():
                    text = " ".join(
                        str(x) for x in row if str(x).strip() != ""
                    )

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

                self.logger.info(f"[OK] Table {table_idx} processed")

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing table {table_idx}: {e}", exc_info=True)

        result = pd.DataFrame(rows)
        result = result.drop_duplicates()

        self.logger.info(f"[END] Total rows extracted: {len(result)}")

        return result


def scrape(route):
    scraper = WLYCPDFScraper()
    return scraper.run(route)