import logging
from app.core.config import LOG_PATH


def get_scraper_logger(name: str):
    logger = logging.getLogger(f"scraper.{name}")

    # Evitar duplicados
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logger.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # 📁 Archivo específico por scraper
        file_handler = logging.FileHandler(LOG_PATH / f"{name}.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        # 📺 Consola
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger