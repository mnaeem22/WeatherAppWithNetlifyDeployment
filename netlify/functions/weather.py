"""
Netlify serverless function: weather API.
Serves /api/weather on Netlify so the frontend can fetch weather without running Flask.
"""
import json
import os
import sys
from pathlib import Path

# Add project root so we can import weather_service
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from weather_service import (
    fetch_weather,
    WeatherServiceError,
    ConfigurationError,
)


def _response(status_code: int, body: dict) -> dict:
    """Netlify function response format."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body),
    }


def handler(event, context):
    """Handle GET /api/weather?city=..."""
    try:
        params = event.get("queryStringParameters") or {}
        city = (params.get("city") or "").strip()

        if not city:
            return _response(400, {"success": False, "error": "City name is required."})

        try:
            data = fetch_weather(city)
            return _response(200, {"success": True, "data": data})
        except ConfigurationError as e:
            return _response(500, {"success": False, "error": str(e)})
        except WeatherServiceError as e:
            return _response(400, {"success": False, "error": str(e)})
        except Exception:
            return _response(
                500,
                {"success": False, "error": "Unexpected error. Please try again later."},
            )
    except Exception:
        return _response(
            500,
            {"success": False, "error": "Unhandled error in weather function."},
        )
