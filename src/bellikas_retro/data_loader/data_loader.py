from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional, Union

import pandas as pd

# Usage:
#
# from pathlib import Path
#
# loader = DataLoader(data_dir=Path("data"))
#
# # Load entire dataset (cached after first call)
# df = loader.load()
#
# # Query by platform
# wii_games = loader.query(platform="Wii")
# console_games = loader.query(platform=["Wii", "PS2", "PS3"])
#
# # Advanced Query
# hits = loader.query(
#     platform=["PS2", "PS3"],
#     year=range(2005, 2011),
#     genre="Action",
# )


@dataclass
class DataLoader:
    """
    Loads a video game sales CSV file and lets you query it.

    The data is only loaded once and then stored in memory so future
    queries are faster.
    """
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
        """
        Returns the full path to the CSV file.
        """
        # Compute the full path to the CSV file.
        return self.data_dir / self.csv_name

    def load(self) -> pd.DataFrame:
        """
        Loads the CSV file into a pandas DataFrame (and caches it).
        """
        # Load the dataset from disk only once.
        # Subsequent calls reuse the cached DataFrame.
        if self._df is None:
            # Read the CSV file into a DataFrame.
            df = pd.read_csv(self.path)

            # Drop empty rows.
            df = df.dropna(how="all")

            # Normalize column names once to avoid repeated cleanup later.
            df.columns = [c.strip() for c in df.columns]

            # Iterate columns whose dtype is object.
            for col in df.select_dtypes(include=["object"]).columns:
                # Strings to pandas’ nullable string dtype -> Strip leading and trailing whitespace -> Convert empty strings into panda missing values.
                df[col] = df[col].astype("string").str.strip().replace("", pd.NA)

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
        """
        Filters the dataset by platform, year, and genre.
        Returns a new DataFrame with only the matching rows.
        """
        # Ensure the dataset is loaded (from cache or disk)
        df = self.load()

        # Normalize filter inputs into sets so .isin() can be used consistently.
        # {"Wii","PS2"}
        # {2000,2001,2002}
        # None
        def _as_set(x):
            """
            Converts a value or list of values into a set.
            Returns None if no value was provided.
            """
            if x is None:
                return None
            if isinstance(x, (str, bytes)):
                return {x}
            return set(x)


        # Convert user-provided filters into sets.
        platforms = _as_set(platform)
        years = _as_set(year)
        genres = _as_set(genre)

        # Start with the full dataset and progressively filter it.
        out = df

        # Apply platform filter if provided.
        if platforms is not None:
            out = out[out["Platform"].isin(platforms)]

        # Apply year filter if provided.
        if years is not None:
            out = out[out["Year"].isin(years)]

        # Apply genre filter if provided.
        if genres is not None:
            out = out[out["Genre"].isin(genres)]

        # Return a new filtered DataFrame with a clean index.
        return out.reset_index(drop=True)