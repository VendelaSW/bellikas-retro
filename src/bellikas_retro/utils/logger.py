"""
Central loggingfil för Bellikas_Retro

"""
import logging
from pathlib import Path

from .config import LOG_LEVEL, PROJECT_ROOT

LOG_DIR = PROJECT_ROOT / 'logs'
LOG_FILE = LOG_DIR / "app.log"

def get_logger(name: str) -> logging.Logger:

    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
