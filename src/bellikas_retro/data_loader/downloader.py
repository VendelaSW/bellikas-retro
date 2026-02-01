from pathlib import Path
from ..utils import PROJECT_ROOT, DATA_DIR, CSV_NAME, KAGGLE_DATASET_PATH, _is_ci
import os
import shutil

from dotenv import load_dotenv
import kagglehub

# Function to download the CSV dataset, call with download_dataset()
def download_dataset() -> None:
    # Hard return if testing (CI/tests should set this and use fixtures)
    # In github workflow file: 
    # set env:
    #   SKIP_DATA_DOWNLOAD: "1"
    if os.getenv("SKIP_DATA_DOWNLOAD", "").strip().lower() in {"1", "true", "yes"}:
        return

    # Local dev only
    if not _is_ci():
        load_dotenv(PROJECT_ROOT / ".env")

    DATA_DIR.mkdir(exist_ok=True)

    destination = DATA_DIR / CSV_NAME
    if destination.exists() and destination.stat().st_size > 0:
        return

    if not os.getenv("KAGGLE_API_TOKEN"):
        raise RuntimeError(
            "Missing KAGGLE_API_TOKEN. Set it in your .env (local dev only)."
        )

    try:
        dataset_dir = Path(kagglehub.dataset_download(KAGGLE_DATASET_PATH))
    except Exception as e:
        raise RuntimeError(f"Dataset download failed for {KAGGLE_DATASET_PATH}") from e

    source = dataset_dir / CSV_NAME

    if not source.exists():
        raise RuntimeError(f"Expected dataset file not found: {source}")

    shutil.copy2(source, destination)


if __name__ == "__main__":
    # For testing only
    download_dataset()
    print("Dataset downloaded successfully")
