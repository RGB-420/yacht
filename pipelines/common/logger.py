import logging

from app.core.config import LOG_PATH


def get_logger(name):
    logger = logging.getLogger(name)

    # Evitar duplicados
    if not logger.handlers:

        logger.setLevel(logging.INFO)
        logger.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # File handler
        file_handler = logging.FileHandler(LOG_PATH / "pipeline.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        # Console handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger