from .helpers import _project_root

CSV_NAME = "vgsales.csv"
PROJECT_ROOT = _project_root()
DATA_DIR = PROJECT_ROOT / "data"
KAGGLE_DATASET_PATH = "gregorut/videogamesales"

SESSION_KEYS = ['region', 'year_range']

NEON_IMAGE_PATH = 'app/static/neonsign.png'

APP_TITLE = "Bellika's Retro: Retro Game Sales Dashboard"

TOGGLE_NOSTALGIA_LABEL = 'Activate Nostalgia Age Filter'
TOGGLE_SALES_LABEL = 'Activate Min Sales Filter'

AGE_INPUT_LABEL = 'Insert Age'
REGION_RADIO_LABEL = 'Select Region to display Sales'
YEAR_SLIDER_LABEL = 'Release Year'

REGIONS = ('NA', 'EU', 'JP', 'OTHER', 'GLOBAL')
REGION_COLUMN_MAP = {
    'NA': 'NA_Sales',
    'EU': 'EU_Sales',
    'JP': 'JP_Sales',
    'OTHER': 'Other_Sales',
    'GLOBAL': 'Global Sales',
}

MIN_AGE = 17 
MAX_AGE = 60
MIN_SALES_DEFAULT = 1.0

import logging
LOG_LEVEL = logging.WARNING
