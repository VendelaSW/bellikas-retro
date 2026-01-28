from __future__ import annotations

import argparse
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import requests

# ---------------------------
# Core: Years set (5–18)
# ---------------------------
def years_when_age_between(birth_year: int, start_age: int = 5, end_age: int = 18) -> set[int]:
    start_year = birth_year + start_age
    end_year = birth_year + end_age
    return set(range(start_year, end_year + 1))


# ---------------------------
# Data model
# ---------------------------
@dataclass(frozen=True)
class Game:
    title: str
    year: int
    raw: Dict[str, Any]  # original API payload for debugging/extra fields 


# ---------------------------
# API Client (adjust to your API)
# ---------------------------
class APIClient:
    """
    Anpassas till ert API.
    Du behöver:
    - base_url
    - ev. api_key
    - hur man skickar params (page/per_page eller offset/limit, osv)
    - hur man tolkar svaret (lista + nästa sida)
    """

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout_s: int = 20,
        sleep_between_requests_s: float = 0.2,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout_s = timeout_s
        self.sleep_s = sleep_between_requests_s
        self.session = requests.Session()

    def fetch_games_page(
        self,
        start_year: int,
        end_year: int,
        page: int,
        page_size: int,
    ) -> Tuple[List[Dict[str, Any]], Optional[int]]:
        """
        Returnerar: (items, next_page)
        - items: lista av "raw" spelobjekt från API:t
        - next_page: nästa sida (int) eller None om slut

        ⚠️ Byt ut detta efter er API-spec.
        """

        # EXEMPEL på generiska query params:
        # ?released_gte=2010&released_lte=2023&page=1&page_size=50
        url = f"{self.base_url}/games"

        params = {
            "released_gte": start_year,
            "released_lte": end_year,
            "page": page,
            "page_size": page_size,
        }

        headers = {}
        if self.api_key:
            # Vanliga mönster är:
            # headers["Authorization"] = f"Bearer {self.api_key}"
            # eller params["key"] = self.api_key
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            resp = self.session.get(url, params=params, headers=headers, timeout=self.timeout_s)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            raise RuntimeError(f"API request failed: {e}") from e
        except ValueError as e:
            raise RuntimeError("API returned non-JSON response.") from e

        # EXEMPEL på generiskt svarformat:
        # { "results": [...], "next_page": 2 } eller { "results": [...], "next": true }
        items = data.get("results", [])
        next_page = data.get("next_page")

        # Om API:t istället har t.ex. "next" som URL eller bool:
        # - Anpassa detta så det matchar ert API.
        if next_page is None:
            # Om API:t t.ex. returnerar total_pages:
            total_pages = data.get("total_pages")
            if isinstance(total_pages, int) and page < total_pages:
                next_page = page + 1

        time.sleep(self.sleep_s)
        return items, next_page

    @staticmethod
    def parse_game(raw: Dict[str, Any]) -> Optional[Game]:
        """
        Gör om API payload -> Game(title, year).
        Anpassa fältnamn efter ert API.
        """
        title = raw.get("name") or raw.get("title")
        released = raw.get("released") or raw.get("release_date") or raw.get("releaseYear")

        # Försök att få år på några vanliga sätt:
        year = None
        if isinstance(released, int):
            year = released
        elif isinstance(released, str) and len(released) >= 4:
            # t.ex. "2017-09-26" eller "2017"
            try:
                year = int(released[:4])
            except ValueError:
                year = None

        if not title or not year:
            return None

        return Game(title=title, year=year, raw=raw)

    def fetch_games_between_years(self, start_year: int, end_year: int, page_size: int = 50, max_pages: int = 50) -> List[Game]:
        games: List[Game] = []
        page = 1
        pages_seen = 0

        while page is not None and pages_seen < max_pages:
            raw_items, next_page = self.fetch_games_page(start_year, end_year, page, page_size)

            for raw in raw_items:
                g = self.parse_game(raw)
                if g:
                    games.append(g)

            pages_seen += 1
            page = next_page

        return games


# ---------------------------
# Matching + output
# ---------------------------
def match_games_to_years(games: List[Game], years: set[int]) -> List[Game]:
    matched = [g for g in games if g.year in years]
    # sortera snyggt
    matched.sort(key=lambda x: (x.year, x.title.lower()))
    return matched


def main():
    parser = argparse.ArgumentParser(description="Age Helper: matcha spel via API mellan åldern 5–18.")
    parser.add_argument("--birth-year", type=int, required=True, help="Födelseår, t.ex. 2005")
    parser.add_argument("--base-url", type=str, required=True, help="Bas-URL till ert API, t.ex. https://api.example.com")
    parser.add_argument("--api-key", type=str, default=None, help="API-nyckel (om behövs)")
    parser.add_argument("--start-age", type=int, default=5, help="Startålder (default 5)")
    parser.add_argument("--end-age", type=int, default=18, help="Slutålder (default 18)")
    parser.add_argument("--page-size", type=int, default=50, help="Antal per sida (default 50)")
    parser.add_argument("--max-pages", type=int, default=50, help="Säkerhetsgräns för max sidor (default 50)")
    args = parser.parse_args()

    years = years_when_age_between(args.birth_year, args.start_age, args.end_age)
    start_year = min(years)
    end_year = max(years)

    print(f"\nÅr-set (när du var {args.start_age}–{args.end_age}):")
    print(sorted(years))
    print(f"\nAPI-hämtning av spel mellan {start_year} och {end_year}...\n")

    client = APIClient(base_url=args.base_url, api_key=args.api_key)
    all_games = client.fetch_games_between_years(start_year, end_year, page_size=args.page_size, max_pages=args.max_pages)
    matched = match_games_to_years(all_games, years)

    if not matched:
        print("Inga spel matchade (eller API:t returnerade inga spel med parsebara år).")
        return

    print(f"Hittade {len(matched)} matchande spel:\n")
    for g in matched:
        print(f"- {g.year}: {g.title}")


if __name__ == "__main__":
    main()
