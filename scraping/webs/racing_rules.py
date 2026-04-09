import pandas as pd
import requests
from bs4 import BeautifulSoup
import tempfile
import os

from app.core.base_scraper import BaseScraper


columnas_fijas = [
    "rank",
    "class",
    "boat",
    "boat_class",
    "sail_number",
    "helm_name",
]

ocr = None

def get_ocr():
    global ocr
    if ocr is None:
        if os.getenv("DISABLE_OCR") == "1":
            raise RuntimeError("OCR disabled")
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang='en')
    return ocr


class RacingRulesScraper(BaseScraper):

    def __init__(self):
        super().__init__("racing_rules")


    def scrape(self, url, browser):
        df = pd.DataFrame()
        page = browser.new_page()

        self.logger.info(f"[STEP] Scraping URL: {url}")

        try:
            html = self.get_html_with_playwright(page, url)

            if html:
                data = self.obtener_partidos(html)

                if data:
                    df_temp = pd.DataFrame(data)
                    df = pd.concat([df, df_temp], ignore_index=True)

                    self.logger.info(f"[OK] Scraped {len(df_temp)} rows")

                else:
                    self.logger.warning("[EMPTY] No boats found")

            else:
                self.logger.error("[FAIL] Could not retrieve HTML")
                return None

        except Exception as e:
            self.logger.error(f"[FAIL] Error in scrape(): {e}", exc_info=True)
            return None

        df = df.drop_duplicates()

        return df


    def get_html_with_playwright(self, page, url: str) -> str:
        try:
            page.goto(url)
            page.wait_for_load_state("networkidle")
            return page.content()
        except Exception as e:
            self.logger.error(f"[FAIL] Error loading {url}: {e}", exc_info=True)
            return None


    def agrupar_por_filas(self, celdas, tolerancia=10):
        filas = []

        for celda in sorted(celdas, key=lambda c: c["y"]):
            encontrada = False
            for fila in filas:
                if abs(fila[0]["y"] - celda["y"]) <= tolerancia:
                    fila.append(celda)
                    encontrada = True
                    break
            if not encontrada:
                filas.append([celda])

        return filas


    def extraer_tabla_desde_imagen(self, url_imagen):
        self.logger.info(f"[STEP] OCR processing image: {url_imagen}")

        ocr_model = get_ocr()

        image_path = None

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url_imagen, headers=headers, timeout=15)

        if response.status_code != 200:
            self.logger.warning(f"[SKIP] Failed to download image: {url_imagen}")
            return pd.DataFrame()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
            f.write(response.content)
            img_path = f.name

        try:
            result = ocr_model.predict(img_path)

            bloque = result[0]
            texts = bloque["rec_texts"]
            boxes = bloque["dt_polys"]

            celdas = []

            for texto, box in zip(texts, boxes):
                xs = [p[0] for p in box]
                ys = [p[1] for p in box]

                celdas.append({
                    "texto": texto,
                    "x": min(xs),
                    "y": min(ys)
                })

            celdas_filtradas = [c for c in celdas if c["y"] > 40]

            filas = self.agrupar_por_filas(celdas_filtradas)

            tabla = []
            for fila in filas:
                fila_ordenada = sorted(fila, key=lambda c: c["x"])
                tabla.append([c["texto"] for c in fila_ordenada])

            tabla_recortada = [fila[:6] for fila in tabla]

            df_tabla = pd.DataFrame(tabla_recortada[1:], columns=columnas_fijas)

            self.logger.info(f"[OK] OCR extracted {len(df_tabla)} rows")

            return df_tabla

        except Exception as e:
            self.logger.error(f"[FAIL] OCR failed: {e}", exc_info=True)
            return pd.DataFrame()
        
        finally:
            if image_path and os.path.exists(img_path):
                os.remove(img_path)


    def obtener_partidos(self, html):
        soup = BeautifulSoup(html, "html.parser")
        tablas = soup.find_all("table", class_="table")

        self.logger.info(f"[INFO] Tables found: {len(tablas)}")

        datos = []

        for table_idx, tabla in enumerate(tablas):
            try:
                filas = tabla.find("tbody").find_all("tr")

                for fila in filas:
                    datos_barco = fila.find_all("td")
                    if not datos_barco:
                        continue

                    course = datos_barco[0].text.strip()

                    if course == "Series Results":
                        link_imagen = datos_barco[6].find("a", href=True)['href']

                        self.logger.info(f"[STEP] Image found: {link_imagen}")

                        df_tabla = self.extraer_tabla_desde_imagen(link_imagen)

                        for _, fila in df_tabla.iterrows():
                            datos.append({
                                "class": fila["class"],
                                "boat": fila["boat"],
                                "type": fila["boat_class"],
                                "boat_number": fila["sail_number"],
                            })

            except Exception as e:
                self.logger.error(f"[FAIL] Error processing table {table_idx}: {e}", exc_info=True)

        self.logger.info(f"[INFO] Total boats extracted: {len(datos)}")

        return datos


def scrape(url, browser):
    scraper = RacingRulesScraper()
    return scraper.run(url, browser)