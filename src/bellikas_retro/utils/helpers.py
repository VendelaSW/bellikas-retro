from pathlib import Path

def _project_root() -> Path:
    here = Path(__file__).resolve()
    for p in (here, *here.parents):
        if (p / "pyproject.toml").exists():
            return p
    raise RuntimeError("Could not locate project root")
# ---------------------------
# nostalgia age: Years set (8–14)
# ---------------------------
def nostalgia_age_filter(age: int, start_age: int = 8, end_age: int = 14) -> set[int]:
    from datetime import datetime
    year = datetime.now().year
    birth_year = year - age
    start_year = birth_year + start_age
    end_year = birth_year + end_age
    return set(range(start_year, end_year + 1))