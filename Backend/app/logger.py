import logging
import os
import sys

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

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(FORMATTER)

    logger.addHandler(handler)
    logger.addHandler(stream_handler)

    return logger

def setup_error_logging():

    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

    handler = logging.FileHandler("logs/error.log", encoding="utf-8")
    handler.setFormatter(FORMATTER)
    handler.setLevel(logging.ERROR)

    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setLevel(logging.ERROR)
    stream_handler.setFormatter(FORMATTER)

    logger.addHandler(handler)
    logger.addHandler(stream_handler)