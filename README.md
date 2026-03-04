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

---

### Deploy to Netlify

1. **Sign in to Netlify**  
   Go to [app.netlify.com](https://app.netlify.com) and log in (or sign up with GitHub).

2. **Add a new site from Git**  
   - Click **Add new site** → **Import an existing project**.  
   - Choose **GitHub** and authorize Netlify if needed.  
   - Select the repo: `mnaeem22/WeatherAppWithNetlifyDeployment` (or your repo name).  
   - If your app lives in a subfolder (e.g. `weather-application`), set **Base directory** to that folder in the build settings.

3. **Build settings**  
   Netlify will use your `netlify.toml`. Confirm:
   - **Build command:** (from `netlify.toml` or leave default).  
   - **Publish directory:** `.` (or as in `netlify.toml`).  
   - **Functions directory:** `netlify/functions`.

4. **Environment variables**  
   In the site: **Site settings** → **Environment variables** → **Add a variable** (or **Add from .env**):
   - **Key:** `OPENWEATHER_API_KEY`  
   - **Value:** your OpenWeatherMap API key  
   - **Scopes:** All (or only Production/Deploy previews as you prefer).  

   Save. Redeploy the site if it already ran without the key.

5. **Deploy**  
   Click **Deploy site**. Netlify will build and deploy. Your site URL will be something like `https://your-site-name.netlify.app`.

6. **Check the app**  
   - Open the site URL. You should see the weather app.  
   - Search for a city; the **Weather** request goes to the Netlify function at `/api/weather`.  
   - If the key was missing, you’ll see an error; add `OPENWEATHER_API_KEY` and redeploy.

**If the repo root is not the app folder**  
If your GitHub repo root is the parent of `weather-application` (e.g. `WeatherAppWithNetlifyDeployment` with a subfolder `weather-application`):
- In Netlify build settings, set **Base directory** to `weather-application`.  
- Then publish directory in `netlify.toml` is relative to that base, so `.` is correct.