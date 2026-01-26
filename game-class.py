from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Mapping, Optional
from datetime import date


def _normalize_text(value: Any) -> str:
    """Normalize text: strip + collapse multiple spaces."""
    if value is None:
        return ""
    s = str(value).strip()
    return " ".join(s.split())


def _to_int_or_none(value: Any) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _to_float(value: Any, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


@dataclass(order=True, slots=True)
class Game:
    """
    Advanced Game model with:
    - validation + normalization
    - flexible era checks
    - nostalgia logic based on "age in years"
    - serialization helpers (to_dict/from_dict/from_row)
    - sortable (rank asc, sales desc)
    """

    # Sort key: rank ascending, sales descending
    sort_index: tuple = field(init=False, repr=False, compare=True)

    rank: int
    name: str
    platform: str
    year: Optional[int] = None
    genre: str = ""
    publisher: str = ""
    sales: float = 0.0  # e.g., in millions

    def __post_init__(self) -> None:
        # Normalize text fields
        self.name = _normalize_text(self.name)
        self.platform = _normalize_text(self.platform)
        self.genre = _normalize_text(self.genre)
        self.publisher = _normalize_text(self.publisher)

        # Rank validation
        if not isinstance(self.rank, int):
            try:
                self.rank = int(self.rank)
            except Exception as e:
                raise TypeError("rank must be an integer") from e
        if self.rank <= 0:
            raise ValueError("rank must be > 0")

        # Year validation (allow None)
        if self.year is not None and not isinstance(self.year, int):
            self.year = _to_int_or_none(self.year)

        if self.year is not None:
            current_year = date.today().year
            # Reasonable bounds + small future tolerance
            if not (1950 <= self.year <= current_year + 2):
                raise ValueError(f"year looks unrealistic: {self.year}")

        # Sales validation
        if not isinstance(self.sales, (int, float)):
            self.sales = _to_float(self.sales, default=0.0)
        self.sales = float(self.sales)
        if self.sales < 0:
            raise ValueError("sales cannot be negative")

        # Sort index
        self.sort_index = (self.rank, -self.sales)

    # -------- Business logic --------

    def is_from_era(
        self,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        *,
        inclusive: bool = True,
    ) -> bool:
        """
        Check if the game's year is within [start_year, end_year].
        - If start_year is None => no lower bound
        - If end_year is None => no upper bound
        - inclusive controls boundary behavior
        """
        if self.year is None:
            return False

        y = self.year

        if start_year is not None:
            if inclusive and y < start_year:
                return False
            if not inclusive and y <= start_year:
                return False

        if end_year is not None:
            if inclusive and y > end_year:
                return False
            if not inclusive and y >= end_year:
                return False

        return True

    def is_nostalgia_game(self, *, years_old: int = 20) -> bool:
        """
        Consider a game a "nostalgia game" if it's at least `years_old` years old.
        Default: 20 years.
        """
        if self.year is None:
            return False
        return (date.today().year - self.year) >= years_old

    def age(self) -> Optional[int]:
        """Return the game's age in years, or None if year is missing."""
        if self.year is None:
            return None
        return date.today().year - self.year

    def matches(
        self,
        text: str,
        *,
        fields: tuple[str, ...] = ("name", "genre", "publisher", "platform"),
    ) -> bool:
        """Simple case-insensitive search across selected fields."""
        q = _normalize_text(text).lower()
        if not q:
            return False

        for f in fields:
            value = getattr(self, f, "")
            if isinstance(value, str) and q in value.lower():
                return True

        return False

    # -------- Serialization --------

    def to_dict(self, *, drop_none: bool = True) -> dict[str, Any]:
        """Export to dict. If drop_none=True, omit keys with None values."""
        d = asdict(self)
        d.pop("sort_index", None)
        if drop_none:
            d = {k: v for k, v in d.items() if v is not None}
        return d

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Game:
        """
        Build a Game from dict/JSON-like data.
        Accepts some alternative key capitalizations.
        """
        rank = data.get("rank", data.get("Rank"))
        name = data.get("name", data.get("Name"))
        platform = data.get("platform", data.get("Platform"))
        year = data.get("year", data.get("Year"))
        genre = data.get("genre", data.get("Genre", ""))
        publisher = data.get("publisher", data.get("Publisher", ""))
        sales = data.get("sales", data.get("Sales", 0.0))

        if rank is None or name is None or platform is None:
            raise ValueError("rank, name, and platform are required fields")

        return cls(
            rank=int(rank),
            name=str(name),
            platform=str(platform),
            year=_to_int_or_none(year),
            genre=str(genre) if genre is not None else "",
            publisher=str(publisher) if publisher is not None else "",
            sales=_to_float(sales, default=0.0),
        )

    @classmethod
    def from_row(cls, row: Any) -> Game:
        """
        Build from a row-like object (e.g., CSV dict, pandas.Series).
        Must be Mapping-like or have to_dict().
        """
        if hasattr(row, "to_dict"):
            row = row.to_dict()
        if isinstance(row, Mapping):
            return cls.from_dict(row)
        raise TypeError("row must be a Mapping (dict-like) or provide to_dict()")

    # -------- Display --------

    def __str__(self) -> str:
        y = self.year if self.year is not None else "unknown year"
        return f"{self.name} ({self.platform}, {y}) — {self.sales}M"

    def __repr__(self) -> str:
        return (
            "Game("
            f"rank={self.rank}, name={self.name!r}, platform={self.platform!r}, "
            f"year={self.year!r}, genre={self.genre!r}, publisher={self.publisher!r}, "
            f"sales={self.sales!r}"
            ")"
        )
