import os
from pathlib import Path
from typing import Dict, Any

import requests
from dotenv import load_dotenv

# Load .env from project root so the key is found regardless of working directory
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_env_path)

OPENWEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherServiceError(Exception):
    """Base exception type for recoverable weather service errors."""


class ConfigurationError(WeatherServiceError):
    """Raised when application configuration is invalid or incomplete."""


class CityNotFoundError(WeatherServiceError):
    """Raised when the requested city cannot be found."""


def _get_api_key() -> str:
    """Return the OpenWeatherMap API key or raise a configuration error."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ConfigurationError(
            "OPENWEATHER_API_KEY is not configured. "
            "Set it in your environment or in Netlify site settings."
        )
    return api_key


def fetch_weather(city: str, units: str = "metric") -> Dict[str, Any]:
    """
    Fetch weather information for the given city using OpenWeatherMap.

    Returns a normalized dictionary suitable for JSON responses.
    Raises WeatherServiceError subclasses for expected error conditions.
    """
    api_key = _get_api_key()

    params = {
        "q": city,
        "appid": api_key,
        "units": units,
    }

    try:
        response = requests.get(OPENWEATHER_API_URL, params=params, timeout=10)
    except requests.RequestException:
        # Any network-level failure is mapped to a user-friendly error
        raise WeatherServiceError(
            "Unable to reach the weather service. Please check your connection and try again."
        )

    # OpenWeatherMap uses HTTP status codes and a 'cod' field in the response body
    if response.status_code == 404:
        raise CityNotFoundError(
            f"Could not find weather information for '{city}'. Please check the city name and try again."
        )

    if not response.ok:
        # Unexpected upstream issue
        raise WeatherServiceError(
            "Weather service is currently unavailable. Please try again later."
        )

    try:
        data = response.json()
    except ValueError:
        raise WeatherServiceError("Received an invalid response from the weather service.")

    # Defensive parsing with safe defaults
    main = data.get("main", {})
    wind = data.get("wind", {})
    weather_list = data.get("weather", []) or [{}]
    weather = weather_list[0] or {}

    temperature = main.get("temp")
    humidity = main.get("humidity")
    wind_speed = wind.get("speed")
    description = weather.get("description", "No description available")

    if temperature is None or humidity is None or wind_speed is None:
        raise WeatherServiceError(
            "Weather data from the service is incomplete. Please try again later."
        )

    # Normalized payload returned to both Flask and Netlify Functions
    return {
        "city": data.get("name", city),
        "temperature": round(temperature, 1),
        "description": description.title(),
        "humidity": humidity,
        "wind_speed": wind_speed,
        "units": "metric",
    }

