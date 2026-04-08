import os
from pathlib import Path

# Base directory (root del proyecto)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Paths desde .env o default
DATA_PATH = Path(os.getenv("DATA_PATH", BASE_DIR / "data"))
LOG_PATH = Path(os.getenv("LOG_PATH", BASE_DIR / "logs"))

# Subcarpetas de datos
DATA_RAW = DATA_PATH / "raw"
DATA_MASTER = DATA_PATH / "master"
DATA_MAPPING = DATA_PATH / "mapping"
DATA_REPORT = DATA_PATH / "report"
DATA_PRENORM = DATA_PATH / "prenormalization"
DATA_SCORECARD = DATA_PATH / "scorecard"

SCRAPERS_LOG_PATH = LOG_PATH / "scrapers"

# Crear carpetas si no existen
DATA_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH.mkdir(parents=True, exist_ok=True)
DATA_RAW.mkdir(parents=True, exist_ok=True)
DATA_MASTER.mkdir(parents=True, exist_ok=True)
DATA_MAPPING.mkdir(parents=True, exist_ok=True)
DATA_REPORT.mkdir(parents=True, exist_ok=True)
DATA_PRENORM.mkdir(parents=True, exist_ok=True)
DATA_SCORECARD.mkdir(parents=True, exist_ok=True)
