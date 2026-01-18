import logging
import os

FORMATTER = logging.Formatter(
         "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

def setup_logging(name: str, archive: str, level=logging.INFO):

    if not os.path.exists("logs"):
        os.mkdir("logs")

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    handler = logging.FileHandler(f"logs/{archive}", encoding="utf-8")
    handler.setLevel(level)
    handler.setFormatter(FORMATTER)

    logger.addHandler(handler)

    return logger

def setup_error_logging():

    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

    handler = logging.FileHandler("logs/error.log", encoding="utf-8")
    handler.formatter(FORMATTER)
    handler.setLevel(logging.ERROR)

    logger.addHandler(handler)