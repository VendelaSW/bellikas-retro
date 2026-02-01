from .helpers import _project_root

CSV_NAME = "vgsales.csv"
PROJECT_ROOT = _project_root()
DATA_DIR = PROJECT_ROOT / "data"
KAGGLE_DATASET_PATH = "gregorut/videogamesales"

import logging
LOG_LEVEL = logging.WARNING
