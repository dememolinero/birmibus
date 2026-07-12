# Birmibus Dashboard - Context for AI Agents

## Project Goal
Dashboard display on **iPad Mini 1st gen running iOS 9.3.5** via Safari. Must be fully functional in old WebKit (no ES6, no modern CSS features).

## Critical Constraint: iOS 9.3.5 Safari
- **NO** `let`, `const`, arrow functions, template literals, `Promise`, `fetch()`, CSS Grid, CSS custom properties
- Use only: `var`, `function`, string concatenation, flexbox with `-webkit-` prefixes, XHR
- Test everything against WebKit from 2016. If it works in modern Chrome but not iOS 9 Safari, it's broken.
- `apple-mobile-web-app-capable` meta tag enabled for fullscreen webapp mode

## Architecture
- **Single file SPA:** `index.html` (~600 lines) — HTML + CSS + JS all embedded
- **No build tools, no frameworks, no dependencies**
- **Data sources:** Open-Meteo (weather), Transport OpenData.ch (departures), RSS2JSON (news)

## File Structure
```
index.html          — Entire application (HTML+CSS+JS)
context.md          — This file (AI context)
skill.md            — Technical reference
tests/test_dashboard.py — Python test suite
```

## Layout (Two-Column Flex)
```
┌─────────────────────┬──────────────────────────────┐
│ col-left (35%)      │ col-right (65%)              │
│                     │                              │
│ ┌─────────────────┐ │ ┌──────────────────────────┐ │
│ │ Clock + Solar   │ │ │ Departures (SBB/Bus)     │ │
│ │ + celestial arc │ │ │ Birmensdorf → Zürich     │ │
│ │ (sunrise/sunset)│ │ │ frequency + delay info   │ │
│ └─────────────────┘ │ └──────────────────────────┘ │
│ ┌─────────────────┐ │                              │
│ │ Calendar        │ │                              │
│ └─────────────────┘ │                              │
│ ┌─────────────────┐ │                              │
│ │ News (rotating) │ │                              │
│ │ 20min + Marca   │ │                              │
│ └─────────────────┘ │                              │
│ ┌─────────────────┐ │                              │
│ │ Weather         │ │                              │
│ │ - Current stats │ │                              │
│ │ - Hourly 5h     │ │                              │
│ │ - Daily 3 days  │ │                              │
│ └─────────────────┘ │                              │
└─────────────────────┴──────────────────────────────┘
```
Mobile: col-left hidden below 560px, col-right takes 100%.

## Color Palette (Apple Dark Theme)
- Background: `#0c0c0e`
- Card background: `#1c1c1e`
- Border: `#2c2c2e`
- Accent/primary: `#ff9f0a` (orange)
- Green (success): `#30d158`
- Red (danger/delay): `#ff453a`
- Blue (info): `#007aff`
- Light blue (precipitation): `#5ac8fa`
- Gray text: `#8e8e93`
- Dimmed: `#3a3a3c`

## Key Functions Reference
| Function | Purpose | Interval |
|----------|---------|----------|
| `updateClock()` | Clock + solar events + arc visibility | 1s |
| `bezierPt(t)` | Quadratic Bezier point for sky arc | — |
| `updateMoonPhase(phase)` | Moon shadow circle for phase icon | — |
| `fmtRemaining(m)` | Time format: "ahora" / "en X min" / "en X h Y min" | — |
| `drawCalendar()` | Monthly calendar | Once on load |
| `fetchWeather()` / `renderWeather()` | Weather data | Once on load |
| `fetchDepartures()` / `renderDeps()` | Train/bus departures + frequency calc | 60s |
| `fetchNews()` / `rotateNews()` | RSS headlines | 900s (15min) |

## Celestial Arc
- SVG with quadratic Bezier curve from (10,60) through (100,-5) to (190,60)
- Sun (orange circle) moves along arc during daylight, hidden at night
- Moon (white circle with shadow) shows lunar phase via SVG shadow offset
- Entire arc hidden when neither sun nor moon visible
- Moon phase calculated from 29.53-day lunar cycle (reference new moon: Jan 6, 2000)

## Solar Data Structure
```javascript
solarData = [
    { type: "sunrise"|"sunset", date: Date_object },
    ...
]  // sorted chronologically
```
Always shows: sunrise 🌅 (left), sunset 🌇 (right).

## Departures: Frequency Calculation
- For each line, calculate interval between first two visible departures
- Round to nearest multiple of 5: `Math.round(interval/5)*5`
- Display "(próximo en X min)" next to the line name
- If next departure has delay, add it to the frequency

## Weather API
```
https://api.open-meteo.com/v1/forecast
  ?latitude=47.3587&longitude=8.4387
  &hourly=temperature_2m,weather_code,apparent_temperature,relative_humidity_2m,wind_speed_10m,precipitation_probability
  &daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_probability_max
  &timezone=Europe%2FZurich&past_days=1&forecast_days=3&current_weather=true
```
Note: `past_days=1` means daily[0]=yesterday, daily[1]=today, daily[2]=tomorrow.

## Transport API
- Station: `Birmensdorf ZH` (train) and `Birmensdorf ZH, Zentrum` (bus)
- Filter: Only connections to Zürich or Schlieren
- Delay detection: yellow/red alerts when delay > 0

## RSS Feeds (via RSS2JSON)
- 20minutos (España/nacional): `https://www.20minutos.es/rss/`
- Marca (Deportes): `https://e00-marca.uecdn.es/rss/portada.xml`

## WMO Weather Code → Emoji
```javascript
var WMO={0:"☀️",1:"🌤️",2:"⛅",3:"☁️",45:"🌫️",48:"🌫️",
    51:"🌧️",53:"🌧️",55:"🌧️",56:"🌧️",57:"🌧️",
    61:"🌧️",63:"🌧️",65:"🌧️",66:"🌧️",67:"🌧️",
    71:"❄️",73:"❄️",75:"❄️",77:"❄️",
    80:"🌧️",81:"🌧️",82:"🌧️",85:"❄️",86:"❄️",
    95:"⛈️",96:"⛈️",99:"⛈️"};
```

## Branches
- `main` — production
- `feature/enhances` — first enhancement batch
- `feature/enhances2` — second enhancement batch
- `feature/enhances3` — third batch (clock arc, forecast fixes)
- `feature/enhances4` — fourth batch (fmtRemaining, next departure, sunset color)
- `feature/enhances5` — fifth batch (RTVE removed, arc hiding, moon phases, frequency fix)

## Testing
- `python3 tests/test_dashboard.py` — unit tests for HTML structure, CSS, JS logic
- No browser automation — visual testing done manually on iPad
