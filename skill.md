# Birmibus Dashboard - Technical Reference

This document serves as a reference for AI agents working on the Birmibus Dashboard project.

## Architecture
- **Single Page Application (SPA):** The entire dashboard is contained within a single `index.html` file.
- **Vanilla JavaScript:** No external frameworks (React, Vue, etc.) are used. UI updates are handled via direct DOM manipulation. **No ES6** — targets iOS 9.3.5 Safari (iPad Mini 1st gen). Use only `var`, `function`, XHR, no arrow functions, no template literals.
- **CSS:** Embedded in the `<style>` tag, using a flexbox-based layout with `-webkit-` prefixes for old WebKit.

## Data Sources
- **Weather:** [Open-Meteo API](https://open-meteo.com/).
  - Coordinates: 47.3587, 8.4387 (Birmensdorf).
  - Forecasts: Hourly (temp, weather code, apparent temp, humidity, wind, precip prob) and Daily (max/min temp, sunrise/sunset, weather code).
  - Note: `past_days=1` means daily[0]=yesterday, daily[1]=today, daily[2]=tomorrow.
- **Public Transport:** [Transport OpenData.ch](https://transport.opendata.ch/).
  - Stations: `Birmensdorf ZH` and `Birmensdorf ZH, Zentrum`.
  - Filtering: Only connections towards Zurich or Schlieren are shown by default.
- **News:** RSS feeds processed via [RSS2JSON](https://rss2json.com/).
  - Current sources: 20minutos, Marca.

## Key Functions
- `updateClock()`: Updates time, date, sunrise/sunset display (always 🌅 left, 🌇 right), celestial arc positions, and arc visibility (hidden when no sun/moon).
- `bezierPt(t)`: Computes x,y on quadratic Bezier for the sky arc visualization.
- `updateMoonPhase(phase)`: Updates SVG shadow circle offset to show lunar phase on the moon icon.
- `fmtRemaining(m)`: Formats minutes as "ahora", "en X min", or "en X h Y min" (for >=60 min).
- `fetchWeather()` / `renderWeather()`: Handles weather data lifecycle. Populates `solarData[]`.
- `fetchDepartures()` / `renderDeps()`: Manages transport data, filtering, and line frequency calculation.
- `fetchNews()` / `rotateNews()`: Fetches RSS feeds and cycles headlines.

## Celestial Arc
- SVG with quadratic Bezier curve: `M10,60 Q100,-5 190,60`
- Sun: orange circle (#ff9f0a), visible only during daylight (sunrise to sunset)
- Moon: white circle (#e5e5ea) with dark shadow (#0c0c0e) showing lunar phase
- Moon phase: `cos(phase * 2π) * 3.5` offset on shadow circle cx
- Arc hidden (`display="none"`) when both sun and moon are below horizon
- Lunar cycle: 29.53059 days, reference new moon: Jan 6, 2000 18:14 UTC

## Departure Frequency
- For each line, calculate interval between first two visible departures
- Round to nearest multiple of 5: `Math.round(interval/5)*5`
- Display "(próximo en X min)" next to the line name in `dep-line` div
- If the next departure has a delay, add it to the frequency

## Layout
- Two-column flex: col-left (35%) + col-right (65%).
- Left column: Clock+Solar arc → Calendar → News → Weather.
- Right column: Transport departures with delay alerts.
- Mobile: col-left hidden below 560px.

## Design Conventions
- **Colors:** Dark theme based on Apple-style system colors (#1c1c1e backgrounds, #ff9f0a accents).
- **Icons:** Uses standard Emojis for weather and transport indicators.
- **Celestial Arc:** SVG with quadratic Bezier curve showing sun (orange) and moon (white+shadow) positions.
