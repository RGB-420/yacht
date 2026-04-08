import camelot
import pandas as pd
from pathlib import Path

from app.core.base_scraper import BaseScraper


class RoyalSolentPDFScraper(BaseScraper):

    def __init__(self):
        super().__init__("royalsolent_pdf")


    def scrape(self, route):
        route = Path(route)

        self.logger.info(f"[STEP] Processing PDF: {route}")

        try:
            tables = camelot.read_pdf(str(route), pages="all", flavor="stream")

            self.logger.info(f"[INFO] Tables detected: {len(tables)}")

        except Exception as e:
            self.logger.error(f"[FAIL] Error reading PDF: {e}", exc_info=True)
            return None

        data = []
        current_class = None

        for table_idx, table in enumerate(tables):
            try:
                df = table.df

                self.logger.info(f"[STEP] Processing table {table_idx} ({len(df)} rows)")

                for i, row in df.iterrows():
                    cell = str(row[0]).strip()

                    if cell.lower().startswith("class"):
                        current_class = cell
                        self.logger.info(f"[CLASS] {current_class}")
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

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing table {table_idx}: {e}", exc_info=True)

        final_df = pd.DataFrame(data)

        self.logger.info(f"[END] Total rows extracted: {len(final_df)}")

        return final_df


def scrape(route):
    scraper = RoyalSolentPDFScraper()
    return scraper.run(route)