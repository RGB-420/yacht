import pandas as pd
import requests
from bs4 import BeautifulSoup
from paddleocr import PaddleOCR

columnas_fijas = [
    "rank",
    "class",
    "boat",
    "boat_class",
    "sail_number",
    "helm_name",
]

ocr = PaddleOCR(use_angle_cls=True, lang='en')

def scrape(url, browser):
    df = pd.DataFrame()
    page = browser.new_page()
            
    html = get_html_with_playwright(page, url)
    if html:
        datos = obtener_partidos(html)
        if datos:
            df_temp = pd.DataFrame(datos)

            df = pd.concat([df, df_temp], ignore_index=True)
        else:
            print("No se encontraron barcos")
    else:
        print("No se pudo obtener el HTML")

    df = df.drop_duplicates()

    return df

def get_html_with_playwright(page, url: str) -> str:
    page.goto(url)
    page.wait_for_load_state("networkidle")
    return page.content()

def obtener_html(session, URL):
    try:
        response = session.get(URL, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error obteniendo {URL}: {e}")
        return None

def agrupar_por_filas(celdas, tolerancia=10):
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

def extraer_tabla_desde_imagen(url_imagen):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url_imagen, headers=headers, timeout=15)

    if response.status_code != 200:
        return []

    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
        f.write(response.content)
        img_path = f.name

    result = ocr.predict(img_path)

    bloque = result[0]

    texts = bloque["rec_texts"]
    boxes = bloque["dt_polys"]

    celdas = []

    for texto, box in zip(texts, boxes):
        # box es un array (4,2)
        xs = [p[0] for p in box]
        ys = [p[1] for p in box]

        celdas.append({
            "texto": texto,
            "x": min(xs),
            "y": min(ys)
        })

    celdas_filtradas = [c for c in celdas if c["y"] > 40]

    filas = agrupar_por_filas(celdas_filtradas)

    tabla = []
    for fila in filas:
        fila_ordenada = sorted(fila, key=lambda c: c["x"])
        tabla.append([c["texto"] for c in fila_ordenada])

    tabla_recortada = [fila[:6] for fila in tabla]

    df_tabla = pd.DataFrame(tabla_recortada[1:], columns=columnas_fijas)

    return df_tabla

def primera_columna_existente(df, columnas):
    for col in columnas:
        if col in df.columns:
            return col
    return None


def obtener_partidos(html):
    soup = BeautifulSoup(html, "html.parser")
    tablas = soup.find_all("table", class_="table")
    print("Tablas encontradas:", len(tablas))

    datos = []

    for tabla in tablas:
        filas = tabla.find("tbody").find_all("tr")

        for fila in filas:
            datos_barco = fila.find_all("td")
            if not datos_barco:
                continue

            course = datos_barco[0].text.strip()

            if course == "Series Results":
                link_imagen = datos_barco[6].find("a", href=True)['href']
                print("Imagen encontrada:", link_imagen)

                # OCR de la imagen
                df_tabla = extraer_tabla_desde_imagen(link_imagen)

                for _, fila in df_tabla.iterrows():
                    datos.append({
                        "class": fila["class"],
                        "boat": fila["boat"],
                        "type": fila["boat_class"],
                        "boat_number": fila["sail_number"],
                    })

    return datos
