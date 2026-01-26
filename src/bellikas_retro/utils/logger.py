"""
Central logging utility for the Bellika Retro Analytics project.

Usage:
    from utils.logger import get_logger
    logger = get_logger(__name__)
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# -------------------------------------------------------------------
# Paths & constants
# -------------------------------------------------------------------

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"

LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# -------------------------------------------------------------------
# Internal setup
# -------------------------------------------------------------------

def _ensure_log_dir() -> None:
    """Create log directory if it does not exist."""
    LOG_DIR.mkdir(exist_ok=True)


def _create_file_handler() -> RotatingFileHandler:
    """Create rotating file handler."""
    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1_000_000,  # 1 MB
        backupCount=3
    )
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    handler.setFormatter(formatter)
    return handler


def _create_console_handler() -> logging.StreamHandler:
    """Create console handler (useful for Streamlit/dev)."""
    handler = logging.StreamHandler()
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    handler.setFormatter(formatter)
    return handler


def _configure_root_logger() -> None:
    """Configure root logger once."""
    _ensure_log_dir()

    root_logger = logging.getLogger()
    if root_logger.handlers:
        return  # Prevent duplicate handlers

    root_logger.setLevel(LOG_LEVEL)
    root_logger.addHandler(_create_file_handler())
    root_logger.addHandler(_create_console_handler())


# -------------------------------------------------------------------
# Public API
# -------------------------------------------------------------------

def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Typically __name__

    Returns:
        logging.Logger
    """
    _configure_root_logger()
    return logging.getLogger(name)
