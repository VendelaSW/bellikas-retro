"""
Central loggingfil för Bellikas_Retro

"""
import logging
from pathlib import Path

# -------------------------------------------------------------------
# Paths & constants
# -------------------------------------------------------------------

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"

# -------------------------------------------------------------------
# Internal setup
# -------------------------------------------------------------------

def get_logger(name: str) -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

# -------------------------------------------------------------------
# Public API
# -------------------------------------------------------------------


    """
    Get a configured logger instance.

    Args:
        name: Typically __name__

    Returns:
        logging.Logger
    """

