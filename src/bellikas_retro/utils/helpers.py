from pathlib import Path
import pandas as pd

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

data = {
    "Name": ["Game A", "Game B", "Game C"],
    "EU_Sales": [1.2, 0.3, 2.5],
    "NA_Sales": [0.8, 1.1, 3.0]
}

df = pd.DataFrame(data)
def filter_sales(df: pd.DataFrame, region: str, minimum: float) -> pd.DataFrame:
    """
    Filtrerar bort rader där sales i vald region är under minimum.
    
    :param df: Pandas DataFrame
    :param region: Kolumnnamn, t.ex. 'EU_Sales'
    :param minimum: Minsta tillåtna värde
    :return: Filtrerad DataFrame
    """
    
    if region not in df.columns:
        raise ValueError(f"Kolumnen '{region}' finns inte i DataFrame")

    filtered_df = df[df[region] >= minimum]
    return filtered_df
filtered = filter_sales(df, "EU_Sales", 1.0)
print(filtered)

import pandas as pd

VALID_REGIONS = {"NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"}

def filter_sales(df: pd.DataFrame, region: str, minimum: float) -> pd.DataFrame:
    if region not in df.columns:
        raise ValueError(f"Kolumnen '{region}' finns inte i DataFrame")
    return df[df[region] >= minimum]


def top_10_games_by_year(
    df: pd.DataFrame,
    year: int,
    region: str = "Global_Sales",
    minimum_sales: float = 0.0,
    year_col: str = "Year",
    name_col: str = "Name",
) -> pd.DataFrame:
    if region not in VALID_REGIONS:
      raise ValueError(f"Region måste vara en av {VALID_REGIONS}")


