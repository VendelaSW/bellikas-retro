from .helpers import _project_root

CSV_NAME = "vgsales.csv"
PROJECT_ROOT = _project_root()
DATA_DIR = PROJECT_ROOT / "data"

import logging
LOG_LEVEL = logging.WARNING
