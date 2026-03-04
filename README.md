## Weather Application (Flask + Netlify)

A production-ready Python 3.11 weather application built with Flask and deployed to Netlify via GitHub Actions.  
Users can enter a city name and see the current temperature, weather description, humidity, and wind speed, backed by the OpenWeatherMap API.

---

### Tech Stack

- **Backend**: Python 3.11, Flask, `requests`, `python-dotenv`
- **Frontend**: HTML, CSS (simple, responsive UI)
- **Deployment**: Netlify (Python serverless function), GitHub Actions CI/CD
- **Weather Data**: OpenWeatherMap API

---

### Features

- **City search**: User enters a city name.
- **Live weather data**: Current temperature, description, humidity, wind speed.
- **Robust error handling**:
  - Invalid or unknown city
  - Network/API failures
  - Missing configuration (API key)
- **UI/UX**:
  - Centered search form
  - Weather results displayed in a card
  - Errors displayed in red, clearly separated from results
  - Mobile-friendly responsive layout

---

### Project Structure

```text
app.py                # Flask app entry point and API route
weather_service.py    # Weather-fetching logic and error handling
requirements.txt      # Python dependencies
runtime.txt           # Python runtime version hint
netlify.toml          # Netlify build and routing configuration
.env.example          # Environment variable template
.gitignore            # Git ignore rules
README.md             # Documentation

templates/
  index.html          # Main HTML UI

static/
  style.css           # Styles for the UI

.github/
  workflows/
    deploy.yml        # GitHub Actions CI/CD pipeline

netlify/
  functions/
    weather.py        # Netlify Python Function for weather API