import os
from pathlib import Path

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from weather_service import (
    fetch_weather,
    WeatherServiceError,
    ConfigurationError,
)


# Load .env from the same directory as this file (project root)
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_env_path)


def create_app() -> Flask:
    """Application factory to create and configure the Flask app."""
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def index():
        """Render the main page with the search form."""
        return render_template("index.html")

    @app.route("/api/weather", methods=["GET"])
    def api_weather():
        """Weather API endpoint used by the frontend (also mirrored by Netlify Function)."""
        city = (request.args.get("city") or "").strip()

        if not city:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "City name is required.",
                    }
                ),
                400,
            )

        try:
            weather_data = fetch_weather(city)
        except ConfigurationError as exc:
            # Configuration problems should be visible but not leak internals
            return jsonify({"success": False, "error": str(exc)}), 500
        except WeatherServiceError as exc:
            # Expected problems like invalid city / upstream issues
            return jsonify({"success": False, "error": str(exc)}), 400
        except Exception:
            # Catch-all for unexpected failures
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Unexpected error while fetching weather. Please try again later.",
                    }
                ),
                500,
            )

        return jsonify({"success": True, "data": weather_data}), 200

    return app


app = create_app()

if __name__ == "__main__":
    # Enable debug only for local development
    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)

