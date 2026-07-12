# Birmibus Dashboard - Technical Reference

This document serves as a reference for AI agents working on the Birmibus Dashboard project.

## Architecture
- **Single Page Application (SPA):** The entire dashboard is contained within a single `index.html` file.
- **Vanilla JavaScript:** No external frameworks (React, Vue, etc.) are used. UI updates are handled via direct DOM manipulation.
- **CSS:** Embedded in the `<style>` tag, using a flexbox-based layout optimized for a 10.1" screen or similar dashboard displays.

## Data Sources
- **Weather:** [Open-Meteo API](https://open-meteo.com/).
  - Coordinates: 47.3587, 8.4387 (Birmensdorf).
  - Forecasts: Hourly (temp, weather code, apparent temp, humidity, wind, precip prob) and Daily (max/min temp, sunrise/sunset, weather code).
- **Public Transport:** [Transport OpenData.ch](https://transport.opendata.ch/).
  - Stations: `Birmensdorf ZH` and `Birmensdorf ZH, Zentrum`.
  - Filtering: Only connections towards Zurich or Schlieren are shown by default.
- **News:** RSS feeds processed via [RSS2JSON](https://rss2json.com/).
  - Current sources: 20minutos, RTVE Deportes, Marca.

## Key Functions
- `updateClock()`: Updates time, date, and handles sunrise/sunset labels ("Amanecer" / "Anochecer").
- `fetchWeather()` / `renderWeather()`: Handles weather data lifecycle.
- `fetchDepartures()` / `renderDeps()`: Manages transport data and filtering.
- `fetchNews()` / `rotateNews()`: Fetches RSS feeds and cycles headlines. **Note:** Ensure intervals are cleared properly when re-fetching to avoid acceleration bugs.

## Design Conventions
- **Colors:** Dark theme based on Apple-style system colors (#1c1c1e backgrounds, #ff9f0a accents).
- **Icons:** Uses standard Emojis for weather and transport indicators.
- **Responsiveness:** Hides the left column on screens smaller than 560px.
