"""
Lab 08: Weather CLI Application

A command-line tool that fetches current weather and forecasts from
WeatherAPI.com and manages a list of favorite locations via JSON persistence.

Usage:
    python lab08.py current <location>
    python lab08.py forecast <location> [--days 1-3]
    python lab08.py favorites add <name> <location>
    python lab08.py favorites list
    python lab08.py favorites remove <name>
"""

import argparse
import json
import os
import sys

try:
    import requests
    _requests_available = True
except ImportError:
    _requests_available = False

# ---------------------------------------------------------------------------
# Configuration — try local config.py first, fall back to environment variable
# ---------------------------------------------------------------------------
try:
    from config import WEATHER_API_KEY, WEATHER_API_BASE_URL
except ImportError:
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "")
    WEATHER_API_BASE_URL = "http://api.weatherapi.com/v1"


# ---------------------------------------------------------------------------
# FavoritesManager
# ---------------------------------------------------------------------------

class FavoritesManager:
    """
    Manages a persistent list of favorite locations stored in a JSON file.

    Parameters
    ----------
    filepath : str or path-like
        Path to the JSON file used for persistence.
    """

    def __init__(self, filepath="favorites.json"):
        self._filepath = filepath
        self._favorites = {}
        self._load()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load(self):
        """Load favorites from the JSON file; start empty on any error."""
        try:
            with open(self._filepath, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, dict):
                # Normalize keys to lowercase on load
                self._favorites = {k.lower(): v for k, v in data.items()}
            else:
                self._favorites = {}
        except FileNotFoundError:
            self._favorites = {}
        except (json.JSONDecodeError, ValueError):
            self._favorites = {}

    def _save(self):
        """Persist the current favorites dict to the JSON file."""
        with open(self._filepath, "w", encoding="utf-8") as fh:
            json.dump(self._favorites, fh, indent=2)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add(self, name, location):
        """
        Add a favorite location.

        Parameters
        ----------
        name : str
            Nickname for the location (case-insensitive key).
        location : str
            Location string (e.g. "Cincinnati, OH").

        Returns
        -------
        bool
            True if added successfully, False if the name already exists.
        """
        key = name.lower()
        if key in self._favorites:
            return False
        self._favorites[key] = location
        self._save()
        return True

    def remove(self, name):
        """
        Remove a favorite by name.

        Parameters
        ----------
        name : str
            Nickname of the favorite to remove (case-insensitive).

        Returns
        -------
        bool
            True if removed, False if the name was not found.
        """
        key = name.lower()
        if key not in self._favorites:
            return False
        del self._favorites[key]
        self._save()
        return True

    def list_all(self):
        """
        Return a copy of all favorites.

        Returns
        -------
        dict
            Mapping of lowercase name -> location string.
        """
        return dict(self._favorites)

    def get_location(self, name):
        """
        Retrieve the location string for a given favorite name.

        Parameters
        ----------
        name : str
            Nickname to look up (case-insensitive).

        Returns
        -------
        str or None
            Location string if found, otherwise None.
        """
        return self._favorites.get(name.lower())


# ---------------------------------------------------------------------------
# WeatherAPI client
# ---------------------------------------------------------------------------

class WeatherAPI:
    """
    Client for the WeatherAPI.com REST API.

    Parameters
    ----------
    api_key : str
        WeatherAPI.com API key.
    base_url : str
        Base URL for the API (default: http://api.weatherapi.com/v1).
    """

    def __init__(self, api_key, base_url=WEATHER_API_BASE_URL):
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")

    def get_current_weather(self, location):
        """
        Fetch current weather for a location.

        Parameters
        ----------
        location : str
            City name, zip code, or coordinates.

        Returns
        -------
        dict or None
            Parsed JSON response, or None on any error.
        """
        if not _requests_available:
            print("Error: 'requests' library is not installed.")
            return None
        url = f"{self._base_url}/current.json"
        params = {"key": self._api_key, "q": location, "aqi": "no"}
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            print(f"Error fetching weather: {exc}")
            return None

    def get_forecast(self, location, days=3):
        """
        Fetch a multi-day weather forecast.

        Parameters
        ----------
        location : str
            City name, zip code, or coordinates.
        days : int
            Number of forecast days (1-3).

        Returns
        -------
        dict or None
            Parsed JSON response, or None on any error.
        """
        if not _requests_available:
            print("Error: 'requests' library is not installed.")
            return None
        days = max(1, min(3, days))
        url = f"{self._base_url}/forecast.json"
        params = {"key": self._api_key, "q": location, "days": days, "aqi": "no"}
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            print(f"Error fetching forecast: {exc}")
            return None


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def format_current_weather(data):
    """
    Format a WeatherAPI current-weather response for console display.

    Parameters
    ----------
    data : dict
        Parsed JSON response from WeatherAPI /current.json endpoint.

    Returns
    -------
    str
        Human-readable formatted string.
    """
    loc = data["location"]
    cur = data["current"]
    city = f"{loc['name']}, {loc['country']}"
    lines = [
        "=" * 50,
        f"Current Weather for {city}",
        "=" * 50,
        f"Condition:    {cur['condition']['text']}",
        f"Temperature:  {cur['temp_f']}°F ({cur['temp_c']}°C)",
        f"Feels Like:   {cur['feelslike_f']}°F ({cur['feelslike_c']}°C)",
        f"Humidity:     {cur['humidity']}%",
        f"Wind:         {cur['wind_mph']} mph {cur['wind_dir']}",
        f"Last Updated: {cur['last_updated']}",
        "=" * 50,
    ]
    return "\n".join(lines)


def format_forecast(data):
    """
    Format a WeatherAPI forecast response for console display.

    Parameters
    ----------
    data : dict
        Parsed JSON response from WeatherAPI /forecast.json endpoint.

    Returns
    -------
    str
        Human-readable formatted string.
    """
    loc = data["location"]
    city = f"{loc['name']}, {loc['country']}"
    sections = [
        "=" * 50,
        f"Forecast for {city}",
        "=" * 50,
    ]
    for day in data["forecast"]["forecastday"]:
        info = day["day"]
        sections += [
            f"\nDate: {day['date']}",
            f"  Condition:  {info['condition']['text']}",
            f"  High/Low:   {info['maxtemp_f']}°F / {info['mintemp_f']}°F"
            f" ({info['maxtemp_c']}°C / {info['mintemp_c']}°C)",
            f"  Humidity:   {info['avghumidity']}%",
            f"  Rain:       {info['daily_chance_of_rain']}% chance",
        ]
    sections.append("=" * 50)
    return "\n".join(sections)


# ---------------------------------------------------------------------------
# CLI command handlers
# ---------------------------------------------------------------------------

_favorites = FavoritesManager()
_api = WeatherAPI(api_key=WEATHER_API_KEY)


def _resolve_location(raw, favorites):
    """Return a location string, resolving favorite names if applicable."""
    resolved = favorites.get_location(raw)
    return resolved if resolved else raw


def cmd_current(args):
    """Handle the 'current' subcommand."""
    location = _resolve_location(args.location, _favorites)
    data = _api.get_current_weather(location)
    if data:
        print(format_current_weather(data))
    else:
        print(f"Could not retrieve weather for '{location}'.")
        sys.exit(1)


def cmd_forecast(args):
    """Handle the 'forecast' subcommand."""
    location = _resolve_location(args.location, _favorites)
    data = _api.get_forecast(location, days=args.days)
    if data:
        print(format_forecast(data))
    else:
        print(f"Could not retrieve forecast for '{location}'.")
        sys.exit(1)


def cmd_favorites_add(args):
    """Handle 'favorites add' subcommand."""
    success = _favorites.add(args.name, args.location)
    if success:
        print(f"Added '{args.name}' -> '{args.location}'")
    else:
        print(f"Favorite '{args.name}' already exists.")


def cmd_favorites_remove(args):
    """Handle 'favorites remove' subcommand."""
    success = _favorites.remove(args.name)
    if success:
        print(f"Removed '{args.name}' from favorites.")
    else:
        print(f"Favorite '{args.name}' not found.")


def cmd_favorites_list(args):
    """Handle 'favorites list' subcommand."""
    all_favs = _favorites.list_all()
    if not all_favs:
        print("No favorites saved yet.")
        return
    print("Saved favorites:")
    for name, location in sorted(all_favs.items()):
        print(f"  {name:<15} -> {location}")


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser():
    """Build and return the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="lab08",
        description="Weather CLI — fetch weather and manage favorite locations.",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    subparsers.required = True

    # -- current -------------------------------------------------------
    current_p = subparsers.add_parser(
        "current", help="Show current weather for a location."
    )
    current_p.add_argument(
        "location", help='City name or favorite name (e.g. "London" or "home").'
    )
    current_p.set_defaults(func=cmd_current)

    # -- forecast -------------------------------------------------------
    forecast_p = subparsers.add_parser(
        "forecast", help="Show weather forecast for a location."
    )
    forecast_p.add_argument(
        "location", help='City name or favorite name (e.g. "Paris" or "work").'
    )
    forecast_p.add_argument(
        "--days",
        type=int,
        default=3,
        choices=[1, 2, 3],
        help="Number of forecast days (1-3, default: 3).",
    )
    forecast_p.set_defaults(func=cmd_forecast)

    # -- favorites -------------------------------------------------------
    favs_p = subparsers.add_parser(
        "favorites", help="Manage favorite locations."
    )
    favs_sub = favs_p.add_subparsers(dest="fav_command", metavar="ACTION")
    favs_sub.required = True

    add_p = favs_sub.add_parser("add", help="Add a new favorite.")
    add_p.add_argument("name", help="Short nickname for the location.")
    add_p.add_argument("location", help='Full location string (e.g. "Cincinnati, OH").')
    add_p.set_defaults(func=cmd_favorites_add)

    list_p = favs_sub.add_parser("list", help="List all saved favorites.")
    list_p.set_defaults(func=cmd_favorites_list)

    remove_p = favs_sub.add_parser("remove", help="Remove a saved favorite.")
    remove_p.add_argument("name", help="Nickname of the favorite to remove.")
    remove_p.set_defaults(func=cmd_favorites_remove)

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    """Parse CLI arguments and dispatch to the appropriate handler."""
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
