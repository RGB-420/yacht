import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from rapidfuzz import process, fuzz
import re

from app.core.base_scraper import BaseScraper


rank_words = ['Rank', 'Pos']

columns_words = {
    "owner": ["owner"],
    "boat": ["yacht", "boat"],
    "number": ["sail number", "sailno", "number"]
}


class J70Scraper(BaseScraper):

    def __init__(self):
        super().__init__("J70")


    def scrape(self, url, browser):
        df = pd.DataFrame()
        df_index = pd.DataFrame()

        page = browser.new_page()

        self.logger.info(f"[STEP] Scraping URL: {url}")

        try:
            links = self.get_links(page, url)
            self.logger.info(f"[INFO] Found {len(links)} iframe links")

            for link in links:
                try:
                    self.logger.info(f"[STEP] Processing link: {link}")

                    html = self.get_html_with_playwright(page, link)

                    if not html:
                        self.logger.warning(f"[SKIP] Could not load HTML for {link}")
                        continue

                    is_final = self.get_index_page(html)

                    headers = self.get_columns(html)

                    if not headers:
                        self.logger.warning("[SKIP] No columns detected")
                        continue

                    column_map = self.get_column_mapping(headers)

                    if is_final:
                        self.logger.info("[INFO] Final results page detected")

                        data = self.obtener_indice(html, column_map)
                        df_index = pd.DataFrame(data)

                    else:
                        data = self.obtener_barcos(html, column_map)

                        df_temp = pd.DataFrame(data)
                        df = pd.concat([df, df_temp], ignore_index=True)

                        self.logger.info(f"[OK] {len(df_temp)} rows extracted")

                except Exception as e:
                    self.logger.error(f"[FAIL] Error processing link {link}: {e}", exc_info=True)

        except Exception as e:
            self.logger.error(f"[FAIL] Error in scrape(): {e}", exc_info=True)
            return None

        if df.empty or df_index.empty:
            self.logger.warning("[WARNING] Missing data for normalization")

        df_clean = self.normalize_data(df, df_index)

        self.logger.info(f"[END] Final cleaned rows: {len(df_clean)}")

        return df_clean[['boat', 'number', 'owner']]


    def get_index_page(self, html):
        soup = BeautifulSoup(html, "html.parser")

        tabla = soup.find("table")
        if not tabla:
            return False

        tbody = tabla.find("tbody")
        if not tbody:
            return False

        rows = tbody.find_all("tr")
        if not rows:
            return False

        first_row = rows[0]
        cell = first_row.find("td", class_="s0")

        if not cell:
            return False

        title = cell.get_text(strip=True)
        return "final" in title.lower()


    def get_links(self, page, url):
        page.goto(url)
        page.wait_for_timeout(3000)

        links = []

        iframe_srcs = page.eval_on_selector_all(
            "iframe",
            "els => els.map(e => e.src).filter(src => src)"
        )

        for iframe in iframe_srcs:
            if re.match(r"^https://docs\.google\.com/spreadsheets", iframe):
                self.logger.info("[INFO] Google Sheets link detected")
                links.append(iframe)
            else:
                self.logger.info(f"[SKIP] Not a valid sheet: {iframe}")

        return links


    def get_html_with_playwright(self, page, url):
        try:
            page.goto(url)
            page.wait_for_timeout(1500)
            return page.content()
        except Exception as e:
            self.logger.error(f"[FAIL] Error loading {url}: {e}", exc_info=True)
            return None


    def get_columns(self, html):
        soup = BeautifulSoup(html, "html.parser")
        tabla = soup.find("table", class_="waffle")

        if not tabla:
            return None

        for row in tabla.find_all("tr"):
            cells = row.find_all("td")
            if not cells:
                continue

            headers = [cell.get_text(strip=True) for cell in cells]
            joined = " ".join(h.lower() for h in headers)

            if any(word.lower() in joined for word in rank_words):
                self.logger.info(f"[INFO] Headers detected: {headers}")
                return headers

        return None


    def get_column_mapping(self, headers):
        mapping = {key: None for key in columns_words}

        for idx, header in enumerate(headers):
            header_norm = header.lower().strip()

            for column_key, keywords in columns_words.items():
                if any(word in header_norm for word in keywords):
                    mapping[column_key] = idx

        self.logger.info(f"[INFO] Column mapping: {mapping}")

        return mapping


    def obtener_barcos(self, html, column_map):
        soup = BeautifulSoup(html, "html.parser")
        tabla = soup.find("table")
        datos = []

        filas = tabla.find("tbody").find_all("tr")

        for fila in filas[2:]:
            datos_barcos = fila.find_all("td")

            def get_value(idx):
                if idx is None or idx >= len(datos_barcos):
                    return None
                return datos_barcos[idx].get_text(strip=True)

            datos.append({
                "boat": get_value(column_map["boat"]),
                "number": get_value(column_map["number"]),
                "owner": get_value(column_map["owner"])
            })

        return datos


    def obtener_indice(self, html, column_map):
        soup = BeautifulSoup(html, "html.parser")
        tabla = soup.find("table")
        datos = []

        filas = tabla.find("tbody").find_all("tr")

        for fila in filas[3:55]:
            datos_barcos = fila.find_all("td")

            def get_value(idx):
                if idx is None or idx >= len(datos_barcos):
                    return None
                return datos_barcos[idx].get_text(strip=True)

            datos.append({
                "boat": get_value(column_map["boat"])
            })

        return datos


    def normalize_data(self, df, df_index):
        df_clean = df.copy()

        df_clean["boat_original"] = df_clean["boat"]
        df_clean["boat"] = df_clean["boat"].apply(self.normalize_boat_name)
        df_clean["boat_norm"] = df_clean["boat"]

        df_clean["number"] = df_clean["number"].apply(self.normalize_sail_number)

        df_index["boat_norm"] = df_index["boat"].apply(self.normalize_boat_name)
        index_names = df_index["boat_norm"].dropna().unique().tolist()

        df_clean = df_clean[
            df_clean["boat"].notna() &
            ~df_clean["boat"].str.contains(
                r"MIXED|YOUTH|OPEN|CORINTHIAN|YACHT|GS#|CATEGORY",
                case=False,
                na=False
            )
        ]

        matches = df_clean["boat_norm"].apply(
            lambda x: self.fuzzy_match_boat(x, index_names)
        )

        df_clean["boat_match"] = matches.apply(lambda x: x[0] if x else None)
        df_clean["match_score"] = matches.apply(lambda x: x[1] if x else 0)

        df_clean["boat"] = np.where(
            df_clean["boat_match"].notna(),
            df_clean["boat_match"],
            df_clean["boat_original"]
        )

        df_clean = df_clean[df_clean["match_score"] >= 85]

        df_clean = (
            df_clean
            .sort_values("match_score", ascending=False)
            .drop_duplicates(subset=["boat"], keep="first")
        )

        return df_clean


    def normalize_boat_name(self, name):
        if pd.isna(name):
            return np.nan
        name = str(name).upper().strip()
        name = name.replace("/", " ")
        name = re.sub(r"[^A-Z0-9 ]", "", name)
        name = re.sub(r"\s+", " ", name)
        return name


    def normalize_sail_number(self, x):
        if pd.isna(x):
            return np.nan
        x = str(x).upper().replace(" ", "")
        if re.fullmatch(r"\d+", x):
            return f"GBR{x}"
        return x


    def fuzzy_match_boat(self, name, index_names, threshold=85):
        if pd.isna(name):
            return None, 0

        match, score, _ = process.extractOne(
            name,
            index_names,
            scorer=fuzz.token_sort_ratio
        )

        if score >= threshold:
            return match, score

        return None, score


def scrape(url, browser):
    scraper = J70Scraper()
    return scraper.run(url, browser)