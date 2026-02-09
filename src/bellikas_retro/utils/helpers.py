from pathlib import Path
import pandas as pd
import os


def _project_root() -> Path:
    here = Path(__file__).resolve()
    for p in (here, *here.parents):
        if (p / "pyproject.toml").exists():
            return p
    raise RuntimeError("Could not locate project root")

def _is_ci() -> bool:
    return os.getenv("CI", "").strip().lower() in {"1", "true", "yes"}


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


def filter_sales(df: pd.DataFrame, region: str, minimum: float) -> pd.DataFrame:
    """   
    Filters out rows where sales in the selected region are below the minimum.
    """
    if region not in df.columns:
        raise ValueError(f"The column '{region}' not in DataFrame")
    return df[df[region] >= minimum]


def top_10_games_by_year(
    df: pd.DataFrame,
    year: int,
    region: str = "Global_Sales",
    minimum_sales: float = 0.0,
    year_col: str = "Year",
    name_col: str = "Name",
) -> pd.DataFrame:
    """
    Returns the top 10 games for a given year, sorted by the selected region,
    and filters out games below minimum_sales.
    """
  
    for col in (year_col, name_col, region):
        if col not in df.columns:
            raise ValueError(f"Missing column '{col}' in DataFrame")

    tmp = df[df[year_col] == year].copy()
    tmp = tmp[tmp[region] >= minimum_sales]
    tmp = tmp.sort_values(by=region, ascending=False).head(10)

    # Optional: return only the most relevant columns
    cols = [name_col, year_col, region]
    return tmp[cols].reset_index(drop=True)
