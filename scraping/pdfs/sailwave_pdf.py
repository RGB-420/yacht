import camelot
import pandas as pd
import numpy as np
from pathlib import Path

from app.core.base_scraper import BaseScraper


columns_map = {
    "owner": ["owner"],
    "boat": ["yacht", "boat"],
    "number": ["sail number", "sailno", "number"],
    "club": ["club"]
}


class SailwavePDFScraper(BaseScraper):

    def __init__(self):
        super().__init__("sailwave_pdf")


    def scrape(self, route):
        route = Path(route)

        self.logger.info(f"[STEP] Processing PDF: {route}")

        try:
            tables = camelot.read_pdf(
                str(route),
                pages="all",
                flavor="stream"
            )

            self.logger.info(f"[INFO] Tables detected: {len(tables)}")

        except Exception as e:
            self.logger.error(f"[FAIL] Error reading PDF: {e}", exc_info=True)
            return None

        dfs = []

        for table_idx, table in enumerate(tables):
            try:
                df = table.df.reset_index(drop=True)

                self.logger.info(f"[STEP] Processing table {table_idx} ({len(df)} rows)")

                header_idx = None

                for i, row in df.iterrows():
                    row_norm = row.astype(str).apply(self.normalize)

                    if any(val in columns_map["number"] for val in row_norm):
                        header_idx = i
                        break

                if header_idx is None:
                    self.logger.warning(f"[SKIP] No header detected in table {table_idx}")
                    continue

                df.columns = df.iloc[header_idx]
                df = df.iloc[header_idx + 1:].reset_index(drop=True)

                df = self.map_columns(df, columns_map)
                df = self.merge_multiline_rows(df)

                df = df[df["number"].astype(str).str.contains(r"\d+", na=False)]

                dfs.append(df)

                self.logger.info(f"[OK] Table {table_idx} processed ({len(df)} rows)")

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing table {table_idx}: {e}", exc_info=True)

        if not dfs:
            self.logger.error("[FAIL] No valid tables extracted from PDF")
            return None

        df_all = pd.concat(dfs, ignore_index=True)

        expected = ["number", "boat", "owner", "club"]
        available = [c for c in expected if c in df_all.columns]

        df_all = df_all[available]
        df_all = df_all.replace({np.nan: None})

        self.logger.info(f"[END] Total rows extracted: {len(df_all)}")

        return df_all


    def normalize(self, col):
        return (
            str(col)
            .lower()
            .strip()
            .replace("\n", " ")
            .replace("\r", " ")
            .replace(".", "")
            .replace("_", " ")
            .replace("-", " ")
            .replace("  ", " ")
        )


    def map_columns(self, df, columns_map):
        new_cols = []

        for col in df.columns:
            norm_col = self.normalize(col)
            mapped = col

            for canonical, aliases in columns_map.items():
                if norm_col in aliases:
                    mapped = canonical
                    break

            new_cols.append(mapped)

        df.columns = new_cols

        self.logger.info(f"[INFO] Mapped columns: {list(df.columns)}")

        return df


    def merge_multiline_rows(self, df):
        rows = []
        current = None

        for _, row in df.iterrows():
            number = str(row.get("number", "")).strip()

            if number and any(char.isdigit() for char in number):
                if current is not None:
                    rows.append(current)
                current = row.to_dict()

            else:
                if current is not None:
                    for col in df.columns:
                        val = str(row[col]).strip()
                        if val and val.lower() != "nan":
                            if current[col] in [None, ""]:
                                current[col] = val
                            else:
                                current[col] += " " + val

        if current is not None:
            rows.append(current)

        result = pd.DataFrame(rows)

        self.logger.info(f"[INFO] Rows after merge: {len(result)}")

        return result


def scrape(route):
    scraper = SailwavePDFScraper()
    return scraper.run(route)