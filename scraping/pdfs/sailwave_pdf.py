import camelot
import pandas as pd
import numpy as np
from pathlib import Path

from app.core.base_scraper import BaseScraper


COLUMN_MAP = {
    "division": ["fleet", "divisione"],
    "sailno": [ "sailno", "sail number", "sail_no", "numvel"],
    "boat": ["boat", "boat name", "barca"],
    "type": ["class", "boat type", "design class"],
    "club": ["club", "yacht club"],
    "owner": ["owner", "helm/owner"],
    "mna": ["boat mna", "naz"],
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
                flavor="lattice"
            )

            self.logger.info(f"[INFO] Tables detected: {len(tables)}")

        except Exception as e:
            self.logger.error(f"[FAIL] Error reading PDF: {e}", exc_info=True)
            return None

        dfs = []

        for table_idx, table in enumerate(tables):

            try:
                self.logger.info(f"[STEP] Processing table {table_idx}")

                df = table.df.reset_index(drop=True)

                header_idx = self.detect_header_row(df)

                if header_idx is None:
                    self.logger.warning(f"[SKIP] No valid header detected")
                    continue

                headers = df.iloc[header_idx].tolist()

                indices = self.get_column_indices(headers)

                cols = self.resolve_columns(indices, COLUMN_MAP)

                df = df.iloc[header_idx + 1:].reset_index(drop=True)

                df = self.extract_rows(df, cols)

                df = self.merge_multiline_rows(df)

                df = df[
                    df["sailno"]
                    .astype(str)
                    .str.contains(r"\d+", na=False)
                ]

                dfs.append(df)

                self.logger.info(f"[OK] Table {table_idx} processed ({len(df)} rows)")

            except Exception as e:
                self.logger.error(
                    f"[FAIL] Error processing table {table_idx}: {e}",
                    exc_info=True
                )

        if not dfs:
            self.logger.error("[FAIL] No valid tables extracted")
            return None

        df_all = pd.concat(dfs, ignore_index=True)

        expected = ["sailno", "boat", "owner", "club"]

        available = [c for c in expected if c in df_all.columns]

        df_all = df_all[available]

        df_all = df_all.replace({np.nan: None})

        self.logger.info(f"[END] Total rows extracted: {len(df_all)}")

        return df_all


    def normalize(self, text):
        return (
            str(text)
            .lower()
            .strip()
            .replace("\n", " ")
            .replace("\r", " ")
            .replace(".", "")
            .replace("_", " ")
            .replace("-", " ")
            .replace("  ", " ")
        )


    def detect_header_row(self, df):

        for i, row in df.iterrows():

            row_norm = [
                self.normalize(v)
                for v in row.tolist()
            ]

            hits = 0

            for aliases in COLUMN_MAP.values():
                if any(alias in row_norm for alias in aliases):
                    hits += 1

            if hits >= 2:
                self.logger.info(
                    f"[INFO] Header detected at row {i}"
                )

                return i

        return None


    def get_column_indices(self, headers):

        col_index = {}

        for i, col in enumerate(headers):

            norm_col = self.normalize(col)

            col_index[norm_col] = i

        self.logger.info(
            f"[INFO] Headers detected: {list(col_index.keys())}"
        )

        return col_index


    def resolve_columns(self, indices, column_map):

        resolved = {}

        for logical_name, possible_headers in column_map.items():

            resolved[logical_name] = None

            for header in possible_headers:

                header = self.normalize(header)

                for detected_header, idx in indices.items():

                    detected_header = self.normalize(detected_header)

                    detected_tokens = detected_header.split()

                    if header in detected_tokens:

                        resolved[logical_name] = idx
                        break

                if resolved[logical_name] is not None:
                    break

        self.logger.info(f"[INFO] Resolved columns: {resolved}")

        return resolved


    def get_cell_value(self, row, idx):

        if idx is None:
            return None

        if idx >= len(row):
            return None

        return row.iloc[idx]


    def extract_rows(self, df, cols):

        rows = []

        for _, row in df.iterrows():

            row_data = {
                key: self.get_cell_value(row, idx)
                for key, idx in cols.items()
            }

            rows.append(row_data)

        return pd.DataFrame(rows)


    def merge_multiline_rows(self, df):

        rows = []

        current = None

        for _, row in df.iterrows():

            number = str(row.get("sailno", "")).strip()

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

        self.logger.info(
            f"[INFO] Rows after merge: {len(result)}"
        )

        return result


def scrape(route):
    scraper = SailwavePDFScraper()
    return scraper.run(route)