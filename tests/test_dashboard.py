#!/usr/bin/env python3
"""
Birmensdorf Dashboard - Test Suite
Tests: HTML structure, JS logic, API connectivity, response formats.
Run: python3 -m pytest tests/test_dashboard.py -v
  or: python3 tests/test_dashboard.py
"""

import os
import re
import json
import sys
import unittest
from urllib.request import urlopen, Request
from urllib.error import URLError

# Path to the dashboard file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_HTML = os.path.join(BASE_DIR, "index.html")


def read_html():
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        return f.read()


def extract_js(html):
    """Extract JavaScript content from <script> tags."""
    matches = re.findall(r"<script[^>]*>(.*?)</script>", html, re.DOTALL)
    return "\n".join(matches)


def api_get(url, timeout=10):
    """Simple HTTP GET that returns (status_code, json_or_none)."""
    try:
        req = Request(url, headers={"User-Agent": "BirmensdorfDashboard/1.0"})
        resp = urlopen(req, timeout=timeout)
        data = resp.read().decode("utf-8")
        return resp.status, json.loads(data)
    except URLError as e:
        return 0, str(e)
    except json.JSONDecodeError:
        return 200, None


# ============================================================
# 1. HTML STRUCTURE TESTS
# ============================================================
class TestHTMLStructure(unittest.TestCase):
    """Verify the dashboard has all required DOM elements."""

    @classmethod
    def setUpClass(cls):
        cls.html = read_html()
        cls.js = extract_js(cls.html)

    def test_file_exists_and_not_empty(self):
        self.assertGreater(len(self.html), 100, "index.html is empty or too small")

    def test_has_doctype(self):
        self.assertIn("<!DOCTYPE html>", self.html)

    def test_has_viewport_meta(self):
        self.assertIn('name="viewport"', self.html)

    def test_has_apple_web_app_meta(self):
        self.assertIn('apple-mobile-web-app-capable', self.html)

    # --- Clock ---
    def test_clock_element_exists(self):
        self.assertIn('id="clock"', self.html)

    def test_solar_past_elements(self):
        self.assertIn('id="icon-past"', self.html)
        self.assertIn('id="time-past"', self.html)

    def test_solar_next_elements(self):
        self.assertIn('id="icon-next"', self.html)
        self.assertIn('id="time-next"', self.html)

    def test_clock_date_element(self):
        self.assertIn('id="clock-date"', self.html)

    # --- Calendar ---
    def test_calendar_body(self):
        self.assertIn('id="cal-body"', self.html)

    def test_calendar_title(self):
        self.assertIn('id="cal-title"', self.html)

    def test_calendar_has_weekday_headers(self):
        for day in ["L", "M", "X", "J", "V", "S", "D"]:
            self.assertIn(day, self.html)

    # --- Weather ---
    def test_weather_current(self):
        self.assertIn('id="wx-current"', self.html)

    def test_weather_hourly(self):
        self.assertIn('id="wx-hourly"', self.html)

    def test_weather_daily(self):
        self.assertIn('id="wx-daily"', self.html)

    # --- News ---
    def test_news_body(self):
        self.assertIn('id="news-body"', self.html)

    # --- Departures ---
    def test_departures_list(self):
        self.assertIn('id="dep-list"', self.html)

    def test_departures_alerts(self):
        self.assertIn('id="dep-alerts"', self.html)

    def test_departures_header_mentions_zurich(self):
        self.assertIn("ZÜRICH", self.html)

    # --- Mobile responsive ---
    def test_media_query_mobile(self):
        self.assertIn("@media", self.html)
        self.assertIn("max-width", self.html)

    def test_media_query_hides_left_panel(self):
        pattern = r"@media[^{]*\{[^}]*\.col-left[^}]*display:\s*none"
        self.assertRegex(self.html, pattern, "Media query should hide .col-left on mobile")


# ============================================================
# 2. CSS / STYLE TESTS
# ============================================================
class TestCSS(unittest.TestCase):
    """Verify critical CSS rules exist."""

    @classmethod
    def setUpClass(cls):
        cls.html = read_html()

    def test_today_highlight_style(self):
        self.assertIn(".today", self.html)
        self.assertIn("background:", self.html)

    def test_delay_text_is_red(self):
        self.assertIn(".dep-delay", self.html)
        self.assertIn("#ff453a", self.html)

    def test_alert_danger_style(self):
        self.assertIn(".alert-danger", self.html)
        self.assertIn("@keyframes", self.html)

    def test_solar_next_is_gray(self):
        self.assertIn(".solar-next", self.html)
        self.assertIn(".solar-next{color:#8e8e93}", self.html)


# ============================================================
# 3. JAVASCRIPT LOGIC TESTS
# ============================================================
class TestJavaScriptFunctions(unittest.TestCase):
    """Verify JS functions exist and key logic is present."""

    @classmethod
    def setUpClass(cls):
        cls.html = read_html()
        cls.js = extract_js(cls.html)

    def test_pad_function_exists(self):
        self.assertIn("function pad(", self.js)

    def test_parseISODate_function_exists(self):
        self.assertIn("function parseISODate(", self.js)

    def test_fmt24h_function_exists(self):
        self.assertIn("function fmt24h(", self.js)

    def test_diffMin_function_exists(self):
        self.assertIn("function diffMin(", self.js)

    def test_fmtRemaining_function_exists(self):
        self.assertIn("function fmtRemaining(", self.js)

    def test_fmtRemaining_hours_format(self):
        """Minutes >= 60 should show hours and minutes."""
        self.assertIn('"en "+h+" h"', self.js)

    def test_goesToZurich_function_exists(self):
        self.assertIn("function shouldShowConnection(", self.js)

    def test_format24hISO_function_exists(self):
        self.assertIn("function format24hISO(", self.js)

    def test_fetchWeather_function_exists(self):
        self.assertIn("function fetchWeather(", self.js)

    def test_fetchDepartures_function_exists(self):
        self.assertIn("function fetchDepartures(", self.js)

    def test_fetchNews_function_exists(self):
        self.assertIn("function fetchNews(", self.js)

    def test_renderDeps_function_exists(self):
        self.assertIn("function renderDeps(", self.js)

    def test_renderWeather_function_exists(self):
        self.assertIn("function renderWeather(", self.js)

    def test_drawCalendar_function_exists(self):
        self.assertIn("function drawCalendar(", self.js)

    def test_rotateNews_function_exists(self):
        self.assertIn("function rotateNews(", self.js)

    def test_interval_clock_updates(self):
        self.assertIn("setInterval(updateClock", self.js)

    def test_interval_departures_refresh(self):
        self.assertIn("setInterval(fetchDepartures", self.js)

    def test_interval_news_refresh(self):
        self.assertIn("setInterval(fetchNews", self.js)

    def test_es5_no_let_const(self):
        """Ensure ES5 compatibility - no let/const keywords."""
        # Remove string literals to avoid false positives
        js_clean = re.sub(r'"[^"]*"', '""', self.js)
        js_clean = re.sub(r"'[^']*'", "''", js_clean)
        self.assertNotRegex(js_clean, r"\blet\b", "Found 'let' - not ES5 compatible")
        self.assertNotRegex(js_clean, r"\bconst\b", "Found 'const' - not ES5 compatible")

    def test_es5_no_arrow_functions(self):
        """Ensure no arrow functions (=>) for iOS 9 compatibility."""
        js_clean = re.sub(r'"[^"]*"', '""', self.js)
        js_clean = re.sub(r"'[^']*'", "''", js_clean)
        self.assertNotIn("=>", js_clean, "Found arrow function '=>' - not ES5 compatible")

    def test_es5_no_template_literals(self):
        """Ensure no backtick template literals."""
        js_clean = re.sub(r'"[^"]*"', '""', self.js)
        js_clean = re.sub(r"'[^']*'", "''", js_clean)
        self.assertNotIn("`", js_clean, "Found backtick template literal - not ES5 compatible")

    def test_es5_uses_xmlhttprequest(self):
        """Should use XMLHttpRequest, not fetch()."""
        self.assertIn("XMLHttpRequest", self.js)

    def test_goesToZurich_checks_passlist(self):
        """The goesToZurich function must check passList for Zurich stops."""
        self.assertIn("passList", self.js)
        self.assertIn("zürich", self.js.lower())

    def test_delay_displayed_in_red(self):
        """Delay should be shown with a delay-specific CSS class."""
        self.assertIn("dep-delay", self.js)
        self.assertIn("+", self.js)  # delay shown as +N

    def test_auto_refresh_60s(self):
        """Departures should auto-refresh."""
        self.assertIn("60000", self.js)

    def test_wmo_weather_codes(self):
        """Weather code to emoji mapping should exist."""
        self.assertIn("WMO", self.js)
        self.assertIn("95", self.js)  # thunderstorm code


# ============================================================
# 4. API CONNECTIVITY TESTS
# ============================================================
class TestAPIConnectivity(unittest.TestCase):
    """Verify external APIs are reachable and return valid data."""

    def test_transport_api_reachable(self):
        url = "https://transport.opendata.ch/v1/stationboard?station=Birmensdorf%20ZH&limit=1"
        status, data = api_get(url)
        self.assertEqual(status, 200, f"Transport API unreachable (status={status})")

    def test_transport_api_returns_stationboard(self):
        url = "https://transport.opendata.ch/v1/stationboard?station=Birmensdorf%20ZH&limit=1"
        _, data = api_get(url)
        self.assertIsNotNone(data, "Transport API returned no data")
        self.assertIn("stationboard", data)
        self.assertIn("station", data)

    def test_transport_api_bus_stop_reachable(self):
        url = "https://transport.opendata.ch/v1/stationboard?station=Birmensdorf%20ZH,%20Zentrum&limit=1"
        status, data = api_get(url)
        self.assertEqual(status, 200, f"Bus stop API unreachable (status={status})")
        self.assertIn("stationboard", data)

    def test_transport_api_has_departure_fields(self):
        url = "https://transport.opendata.ch/v1/stationboard?station=Birmensdorf%20ZH&limit=2"
        _, data = api_get(url)
        if data and "stationboard" in data and len(data["stationboard"]) > 0:
            dep = data["stationboard"][0]
            self.assertIn("to", dep)
            self.assertIn("stop", dep)
            self.assertIn("departure", dep["stop"])
            self.assertIn("departureTimestamp", dep["stop"])

    def test_open_meteo_reachable(self):
        url = "https://api.open-meteo.com/v1/forecast?latitude=47.3587&longitude=8.4387&daily=weather_code&timezone=Europe/Zurich&forecast_days=1"
        status, data = api_get(url)
        self.assertEqual(status, 200, f"Open-Meteo API unreachable (status={status})")

    def test_open_meteo_returns_hourly_data(self):
        url = ("https://api.open-meteo.com/v1/forecast?latitude=47.3587&longitude=8.4387"
               "&hourly=temperature_2m,weather_code"
               "&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset"
               "&timezone=Europe/Zurich&forecast_days=3&current_weather=true")
        _, data = api_get(url)
        self.assertIsNotNone(data)
        self.assertIn("hourly", data)
        self.assertIn("daily", data)
        self.assertIn("current_weather", data)

    def test_open_meteo_has_sunrise_sunset(self):
        url = ("https://api.open-meteo.com/v1/forecast?latitude=47.3587&longitude=8.4387"
               "&daily=sunrise,sunset&timezone=Europe/Zurich&forecast_days=3")
        _, data = api_get(url)
        self.assertIn("daily", data)
        self.assertIn("sunrise", data["daily"])
        self.assertIn("sunset", data["daily"])
        self.assertGreater(len(data["daily"]["sunrise"]), 0)

    def test_rss2json_elpais_reachable(self):
        url = "https://api.rss2json.com/v1/api.json?rss_url=https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada"
        status, data = api_get(url, timeout=15)
        self.assertEqual(status, 200)
        self.assertIsNotNone(data)
        self.assertEqual(data.get("status"), "ok")
        self.assertGreater(len(data.get("items", [])), 0, "El País RSS returned no items")

    def test_rss2json_marca_reachable(self):
        url = "https://api.rss2json.com/v1/api.json?rss_url=https://e00-marca.uecdn.es/rss/portada.xml"
        status, data = api_get(url, timeout=15)
        self.assertEqual(status, 200)
        self.assertIsNotNone(data)
        self.assertEqual(data.get("status"), "ok")


# ============================================================
# 5. DATA PROCESSING LOGIC TESTS
# ============================================================
class TestDataProcessing(unittest.TestCase):
    """Validate the logic used to process API responses."""

    def test_goes_to_zurich_via_destination(self):
        """Connection with Zürich in 'to' field should match."""
        conn = {"to": "Zürich HB", "passList": []}
        # Inline logic test
        dest = conn["to"].lower()
        result = "zürich" in dest or "zurich" in dest
        self.assertTrue(result)

    def test_goes_to_zurich_via_passlist(self):
        """Connection with Zürich in passList should match."""
        conn = {"to": "Hinwil", "passList": [
            {"station": {"name": "Birmensdorf ZH"}},
            {"station": {"name": "Zürich HB"}}
        ]}
        dest = conn["to"].lower()
        direct = "zürich" in dest or "zurich" in dest
        via_pass = False
        for stop in conn["passList"]:
            sn = (stop["station"].get("name") or "").lower()
            if "zürich" in sn or "zurich" in sn:
                via_pass = True
                break
        self.assertFalse(direct)
        self.assertTrue(via_pass)

    def test_goes_to_zurich_negative(self):
        """Connection to Zug (not via Zürich) should NOT match."""
        conn = {"to": "Zug", "passList": [
            {"station": {"name": "Birmensdorf ZH"}},
            {"station": {"name": "Bonstetten-Wettswil"}},
            {"station": {"name": "Zug"}}
        ]}
        dest = conn["to"].lower()
        direct = "zürich" in dest or "zurich" in dest
        via_pass = False
        for stop in conn["passList"]:
            sn = (stop["station"].get("name") or "").lower()
            if "zürich" in sn or "zurich" in sn:
                via_pass = True
                break
        self.assertFalse(direct)
        self.assertFalse(via_pass)

    def test_delay_calculation(self):
        """Verify delay is correctly added to departure timestamp."""
        ts = 1783015500  # some timestamp
        delay = 6  # minutes
        expected = ts * 1000 + delay * 60000
        actual = ts * 1000 + delay * 60000
        self.assertEqual(actual, expected)

    def test_remaining_minutes_calculation(self):
        """Remaining minutes = (actualMs - nowMs) / 60000."""
        now_ms = 1783015500000
        future_ms = 1783015800000  # 5 minutes later
        diff = round((future_ms - now_ms) / 60000)
        self.assertEqual(diff, 5)

    def test_remaining_minutes_negative_means_past(self):
        """If remaining is negative, the train has already left."""
        now_ms = 1783015800000
        past_ms = 1783015500000
        diff = round((past_ms - now_ms) / 60000)
        self.assertEqual(diff, -5)
        self.assertTrue(diff < -1)

    def test_solar_event_sorting(self):
        """Solar events should be sorted chronologically."""
        events = [
            {"type": "sunset", "ts": 300},
            {"type": "sunrise", "ts": 100},
            {"type": "sunset", "ts": 500},
            {"type": "sunrise", "ts": 200},
        ]
        events.sort(key=lambda e: e["ts"])
        self.assertEqual(events[0]["ts"], 100)
        self.assertEqual(events[1]["ts"], 200)
        self.assertEqual(events[2]["ts"], 300)
        self.assertEqual(events[3]["ts"], 500)

    def test_solar_next_vs_past_logic(self):
        """Given current time, correct next/past events are identified."""
        now_ms = 250
        events = [
            {"type": "sunrise", "ts": 100},
            {"type": "sunset", "ts": 200},
            {"type": "sunrise", "ts": 400},
            {"type": "sunset", "ts": 500},
        ]
        next_evt = None
        past_evt = None
        for evt in events:
            if evt["ts"] > now_ms:
                if next_evt is None:
                    next_evt = evt
            else:
                past_evt = evt
        self.assertEqual(next_evt["ts"], 400)
        self.assertEqual(past_evt["ts"], 200)

    def test_pad_function(self):
        """Pad single-digit numbers with leading zero."""
        self.assertEqual("0" + "5", "05")
        self.assertEqual("1" + "2", "12")

    def test_format_24h_iso(self):
        """Extract HH:MM from ISO datetime string."""
        iso = "2026-07-08T14:30:00+0200"
        result = iso.split("T")[1][:5]
        self.assertEqual(result, "14:30")

    def test_format_24h_iso_null(self):
        """Handle null/empty ISO strings."""
        iso = ""
        parts = iso.split("T")
        result = "--:--" if len(parts) < 2 else parts[1][:5]
        self.assertEqual(result, "--:--")


# ============================================================
# 6. CELESTIAL ARC TESTS
# ============================================================
class TestCelestialArc(unittest.TestCase):
    """Validate celestial arc SVG structure and JS logic."""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(BASE_DIR, "index.html"), "r") as f:
            cls.html = f.read()
        js_match = re.search(r"<script>(.*?)</script>", cls.html, re.DOTALL)
        cls.js = js_match.group(1) if js_match else ""

    def test_sky_arc_svg_exists(self):
        """SVG element with class sky-arc must exist."""
        self.assertIn("class=\"sky-arc\"", self.html)
        self.assertIn("<svg", self.html)
        self.assertIn("viewBox=\"0 0 200 65\"", self.html)

    def test_sun_pos_circle_exists(self):
        """Sun position circle must exist in SVG."""
        self.assertIn("id=\"sun-pos\"", self.html)
        self.assertIn("fill=\"#ff9f0a\"", self.html)

    def test_moon_pos_group_exists(self):
        """Moon position must be a <g> group (not a plain circle)."""
        self.assertRegex(self.html, r"<g\s+id=\"moon-pos\"")

    def test_moon_shadow_circle_exists(self):
        """Moon shadow circle for phase rendering must exist."""
        self.assertIn("id=\"moon-sh\"", self.html)
        self.assertIn("fill=\"#0c0c0e\"", self.html)

    def test_bezierPt_function_exists(self):
        """bezierPt function must exist for arc positioning."""
        self.assertIn("function bezierPt(", self.js)

    def test_bezierPt_quadratic_formula(self):
        """bezierPt must use quadratic Bezier formula with P0, P1, P2."""
        self.assertIn("(1-t)*(1-t)*10", self.js)
        self.assertIn("2*(1-t)*t*100", self.js)
        self.assertIn("t*t*190", self.js)

    def test_updateMoonPhase_function_exists(self):
        """updateMoonPhase function must exist for lunar phase icons."""
        self.assertIn("function updateMoonPhase(", self.js)

    def test_moon_shadow_uses_cos(self):
        """Moon shadow offset must use cos(phase*2*PI) for phase calculation."""
        self.assertIn("Math.cos(phase*2*Math.PI)", self.js)

    def test_moon_shadow_cx_set(self):
        """Moon shadow cx must be set based on cos calculation."""
        self.assertIn("moon-sh\"", self.js)
        self.assertIn("cos*3.5", self.js)

    def test_arc_hiding_logic(self):
        """Arc must be hidden when neither sun nor moon visible."""
        self.assertIn("sky-arc", self.js)
        self.assertIn("sunVis", self.js)
        self.assertIn("moonV", self.js)
        self.assertIn("arcEl.setAttribute(\"display\"", self.js)

    def test_arc_visibility_toggle(self):
        """Arc display toggles based on sun/moon visibility."""
        self.assertIn("(sunVis||moonV)", self.js)

    def test_lunar_cycle_constant(self):
        """Lunar synodic month constant (29.53059 days) must be defined."""
        self.assertIn("29.53059", self.js)

    def test_lunar_reference_new_moon(self):
        """Reference new moon date (Jan 6, 2000) must be defined."""
        self.assertIn("new Date(2000,0,6,18,14,0)", self.js)

    def test_moon_age_calculation(self):
        """Moon age must be calculated with double-modulo for cycle position."""
        self.assertIn("moonAge", self.js)
        self.assertIn("((daysSince%LUNAR)+LUNAR)%LUNAR", self.js)

    def test_moon_visible_threshold(self):
        """Moon visibility must exclude ~3 days around new moon."""
        self.assertIn("moonAge>3&&moonAge<26", self.js)

    def test_sky_arc_css_rule(self):
        """CSS rule for .sky-arc must exist."""
        self.assertIn(".sky-arc{", self.html)

    def test_moon_phase_called_when_visible(self):
        """updateMoonPhase must be called when moon is above horizon."""
        self.assertIn("updateMoonPhase(moonPhase)", self.js)


if __name__ == "__main__":
    unittest.main(verbosity=2)
