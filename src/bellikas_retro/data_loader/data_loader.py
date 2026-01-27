from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional, Union

import pandas as pd

# Usage:
# loader = DataLoader(data_dir=Path("data"))
#
# # Load entire dataset (cached after first call)
# df = loader.load()
#
# # Query by platform
# wii_games = loader.query(platform="Wii")


@dataclass
class DataLoader:
    # Directory containing the dataset.
    data_dir: Path

    # Name of the CSV file.
    csv_name: str = "vgsales.csv"

    # Internal cache for the loaded DataFrame:
    # - default=None → data not loaded yet
    # - init=False   → not part of the constructor
    # - repr=False   → excluded from __repr__ to avoid printing a huge DataFrame
    _df: Optional[pd.DataFrame] = field(default=None, init=False, repr=False)

    @property
    def path(self) -> Path:
        # Compute the full path to the CSV file.
        return self.data_dir / self.csv_name

    def load(self) -> pd.DataFrame:
        # Load the dataset from disk only once.
        # Subsequent calls reuse the cached DataFrame.
        if self._df is None:
            # Read the CSV file into a DataFrame.
            df = pd.read_csv(self.path)

            # Normalize column names once to avoid repeated cleanup later.
            df.columns = [c.strip() for c in df.columns]

            # Convert Year to a numeric, nullable integer type to prevent malformed year values.
            if "Year" in df.columns:
                df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")

            # Cache the loaded DataFrame for future queries.
            self._df = df

        # Always return the cached DataFrame.
        return self._df

    def query(
        self,
        # Accept a single value or multiple values for each filter.
        platform: Optional[Union[str, Iterable[str]]] = None,
        year: Optional[Union[int, Iterable[int], range]] = None,
        genre: Optional[Union[str, Iterable[str]]] = None,
    ) -> pd.DataFrame:
        # Ensure the dataset is loaded (from cache or disk)
        df = self.load()

        # Normalize filter inputs into sets so .isin() can be used consistently
        def _as_set(x):
            if x is None:
                return None
            if isinstance(x, (str, bytes)):
                return {x}
            if isinstance(x, range):
                return set(x)
            return set(x)

        # Convert user-provided filters into sets
        platforms = _as_set(platform)
        years = _as_set(year)
        genres = _as_set(genre)

        # Start with the full dataset and progressively filter it
        out = df

        # Apply platform filter if provided
        if platforms is not None:
            out = out[out["Platform"].isin(platforms)]

        # Apply year filter if provided
        if years is not None:
            out = out[out["Year"].isin(years)]

        # Apply genre filter if provided
        if genres is not None:
            out = out[out["Genre"].isin(genres)]

        # Return a filtered COPY with a clean index.
        return out.reset_index(drop=True)