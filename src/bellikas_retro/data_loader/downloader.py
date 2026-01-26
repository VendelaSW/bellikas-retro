from pathlib import Path
import os
import shutil

from dotenv import load_dotenv
import kagglehub
import pandas as pd


# Move to utils/helpers.py
def _project_root() -> Path:
    here = Path(__file__).resolve()
    for p in (here, *here.parents):
        if (p / "pyproject.toml").exists():
            return p
    raise RuntimeError("Could not locate project root")


# Move to config
CSV_NAME = "vgsales.csv"
PROJECT_ROOT = _project_root()
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# Move to github env and workflow
load_dotenv(PROJECT_ROOT / ".env")


def download_dataset() -> pd.DataFrame:
    if not os.getenv("KAGGLE_API_TOKEN"):
        raise RuntimeError("Missing KAGGLE_API_TOKEN")

    dataset_dir = Path(kagglehub.dataset_download("gregorut/videogamesales"))

    source = dataset_dir / CSV_NAME
    destination = DATA_DIR / CSV_NAME

    if not source.exists():
        raise RuntimeError(f"Expected dataset file not found: {source}")

    if not destination.exists():
        shutil.copy2(source, destination)

    return pd.read_csv(destination)


if __name__ == "__main__":
    df = download_dataset()
    print(df.head())