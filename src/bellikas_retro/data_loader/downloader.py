from pathlib import Path
import kagglehub

# Move to config
def _project_root() -> Path:
    here = Path(__file__).resolve()
    for p in (here, *here.parents):
        if (p / "pyproject.toml").exists():
            return p
    raise RuntimeError("Could not locate project root")

PROJECT_ROOT = _project_root()
DATA_DIR = PROJECT_ROOT / "data"


def download_dataset():
    return