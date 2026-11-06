"""
Oasis Infobyte Internship - Python Development
Task 4: Basic Weather App
Author: Silambarasan (OIBSIP Intern)
Description: A production-ready weather application integrating the OpenWeatherMap
             API. Supports city and postal code lookups, dual °C/°F units, error handling,
             an interactive CLI mode, an offline demonstration fallback mode, and a
             modern Tkinter Graphical User Interface (GUI).
"""

import argparse
import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

# Optional requests library import; falls back seamlessly to standard urllib
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Constants
DEFAULT_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"
ENV_API_KEY_NAME = "OPENWEATHER_API_KEY"

# Weather condition icon mapping
WEATHER_ICONS = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌫️",
    "Haze": "🌫️",
    "Smoke": "💨",
    "Dust": "🌪️",
}


@dataclass
class WeatherReport:
    """Structured data model for weather report attributes."""
    city_name: str
    country: str
    temp_c: float
    temp_f: float
    feels_like_c: float
    feels_like_f: float
    humidity: int
    wind_speed_mps: float
    wind_speed_kmh: float
    wind_speed_mph: float
    condition: str
    description: str
    pressure_hpa: int
    visibility_km: float
    timestamp: str
    is_demo: bool = False


# =====================================================================
# Offline Demo / Fallback Meteorological Mock Data
# =====================================================================

MOCK_METEOROLOGY_DATA: Dict[str, Dict[str, Any]] = {
    "chennai": {
        "name": "Chennai",
        "sys": {"country": "IN"},
        "main": {"temp": 31.4, "feels_like": 36.2, "humidity": 78, "pressure": 1012},
        "weather": [{"main": "Clouds", "description": "scattered clouds"}],
        "wind": {"speed": 4.1},
        "visibility": 9000,
    },
    "mumbai": {
        "name": "Mumbai",
        "sys": {"country": "IN"},
        "main": {"temp": 29.8, "feels_like": 34.0, "humidity": 72, "pressure": 1011},
        "weather": [{"main": "Haze", "description": "haze with moderate humidity"}],
        "wind": {"speed": 3.6},
        "visibility": 7000,
    },
    "delhi": {
        "name": "Delhi",
        "sys": {"country": "IN"},
        "main": {"temp": 26.2, "feels_like": 26.5, "humidity": 55, "pressure": 1015},
        "weather": [{"main": "Clear", "description": "clear sunny sky"}],
        "wind": {"speed": 2.8},
        "visibility": 8000,
    },
    "bangalore": {
        "name": "Bengaluru",
        "sys": {"country": "IN"},
        "main": {"temp": 24.5, "feels_like": 24.8, "humidity": 65, "pressure": 1014},
        "weather": [{"main": "Clouds", "description": "pleasant overcast clouds"}],
        "wind": {"speed": 3.2},
        "visibility": 10000,
    },
    "london": {
        "name": "London",
        "sys": {"country": "GB"},
        "main": {"temp": 14.2, "feels_like": 13.5, "humidity": 82, "pressure": 1016},
        "weather": [{"main": "Rain", "description": "light intermittent drizzle"}],
        "wind": {"speed": 5.2},
        "visibility": 8000,
    },
    "new york": {
        "name": "New York",
        "sys": {"country": "US"},
        "main": {"temp": 18.6, "feels_like": 18.2, "humidity": 58, "pressure": 1020},
        "weather": [{"main": "Clear", "description": "clear blue sky"}],
        "wind": {"speed": 4.5},
        "visibility": 10000,
    },
    "tokyo": {
        "name": "Tokyo",
        "sys": {"country": "JP"},
        "main": {"temp": 20.1, "feels_like": 19.8, "humidity": 64, "pressure": 1018},
        "weather": [{"main": "Clouds", "description": "broken clouds"}],
        "wind": {"speed": 3.8},
        "visibility": 10000,
    },
    "paris": {
        "name": "Paris",
        "sys": {"country": "FR"},
        "main": {"temp": 16.4, "feels_like": 15.9, "humidity": 70, "pressure": 1019},
        "weather": [{"main": "Clouds", "description": "overcast clouds"}],
        "wind": {"speed": 3.1},
        "visibility": 10000,
    },
}


# =====================================================================
# Core Logic & Network Operations
# =====================================================================

def convert_celsius_to_fahrenheit(celsius: float) -> float:
    """Converts a Celsius temperature value to Fahrenheit."""
    return round((celsius * 9.0 / 5.0) + 32.0, 2)


def convert_mps_to_kmh(speed_mps: float) -> float:
    """Converts meters per second to kilometers per hour."""
    return round(speed_mps * 3.6, 2)


def convert_mps_to_mph(speed_mps: float) -> float:
    """Converts meters per second to miles per hour."""
    return round(speed_mps * 2.23694, 2)


def parse_weather_payload(payload: Dict[str, Any], is_demo: bool = False) -> WeatherReport:
    """
    Parses OpenWeatherMap JSON payload into a validated WeatherReport object.

    Args:
        payload: JSON dictionary from OpenWeatherMap API.
        is_demo: Flag indicating whether report came from fallback mock.

    Returns:
        WeatherReport dataclass.

    Raises:
        KeyError: If mandatory keys are absent in payload.
        ValueError: If payload data values are invalid.
    """
    if not isinstance(payload, dict):
        raise ValueError("Weather data payload must be a dictionary.")

    try:
        city_name = payload.get("name", "Unknown Location")
        sys_data = payload.get("sys", {})
        country = sys_data.get("country", "--")

        main_data = payload["main"]
        temp_c = float(main_data["temp"])
        feels_like_c = float(main_data.get("feels_like", temp_c))
        humidity = int(main_data["humidity"])
        pressure = int(main_data.get("pressure", 1013))

        weather_list = payload.get("weather", [])
        if weather_list and isinstance(weather_list, list):
            condition = weather_list[0].get("main", "Clear")
            description = weather_list[0].get("description", "clear sky").capitalize()
        else:
            condition = "Clear"
            description = "Clear sky"

        wind_data = payload.get("wind", {})
        wind_speed_mps = float(wind_data.get("speed", 0.0))

        # Visibility in meters to kilometers
        visibility_m = payload.get("visibility", 10000)
        visibility_km = round(visibility_m / 1000.0, 1)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return WeatherReport(
            city_name=city_name,
            country=country,
            temp_c=round(temp_c, 1),
            temp_f=convert_celsius_to_fahrenheit(temp_c),
            feels_like_c=round(feels_like_c, 1),
            feels_like_f=convert_celsius_to_fahrenheit(feels_like_c),
            humidity=humidity,
            wind_speed_mps=round(wind_speed_mps, 1),
            wind_speed_kmh=convert_mps_to_kmh(wind_speed_mps),
            wind_speed_mph=convert_mps_to_mph(wind_speed_mps),
            condition=condition,
            description=description,
            pressure_hpa=pressure,
            visibility_km=visibility_km,
            timestamp=timestamp,
            is_demo=is_demo,
        )
    except (KeyError, TypeError) as err:
        raise ValueError(f"Malformed weather payload received: Missing {err}")


def get_mock_weather(query: str) -> WeatherReport:
    """
    Returns realistic fallback weather report for offline demonstration or testing.
    """
    cleaned = query.strip().lower().split(",")[0].strip()
    data = MOCK_METEOROLOGY_DATA.get(cleaned)

    if not data:
        # Generate a realistic mock based on query name
        data = {
            "name": query.strip().title(),
            "sys": {"country": "INTL"},
            "main": {"temp": 25.0, "feels_like": 26.2, "humidity": 60, "pressure": 1013},
            "weather": [{"main": "Clear", "description": "clear skies (demo data)"}],
            "wind": {"speed": 3.5},
            "visibility": 10000,
        }

    return parse_weather_payload(data, is_demo=True)


def fetch_weather(
    query: str,
    api_key: Optional[str] = None,
    units: str = "metric",
    use_demo: bool = False,
    timeout_sec: int = 8,
) -> WeatherReport:
    """
    Fetches real-time weather information from OpenWeatherMap API with automatic
    fallback to mock data when API key is missing or offline demo is requested.

    Args:
        query: City name (e.g. 'London', 'Chennai,IN') or Postal code.
        api_key: OpenWeatherMap API key (optional; reads env if omitted).
        units: Temperature units ('metric' for Celsius, 'imperial' for Fahrenheit).
        use_demo: Explicit flag to use mock demo mode.
        timeout_sec: Network request timeout in seconds.

    Returns:
        WeatherReport object.

    Raises:
        ValueError: If city is empty or invalid.
        LookupError: If city is not found (404).
        PermissionError: If API key is invalid or unauthorized (401).
        ConnectionError: If network connectivity fails.
    """
    cleaned_query = query.strip()
    if not cleaned_query:
        raise ValueError("Please provide a valid city name or postal code.")

    resolved_key = api_key or os.getenv(ENV_API_KEY_NAME, "").strip()

    if use_demo or not resolved_key or resolved_key.lower() == "demo":
        return get_mock_weather(cleaned_query)

    params = {
        "q": cleaned_query,
        "appid": resolved_key,
        "units": units,
    }
    encoded_query = urllib.parse.urlencode(params)
    full_url = f"{DEFAULT_API_ENDPOINT}?{encoded_query}"

    try:
        if HAS_REQUESTS:
            response = requests.get(full_url, timeout=timeout_sec)
            status_code = response.status_code
            try:
                payload = response.json()
            except Exception:
                raise ConnectionError("Invalid JSON response received from API server.")
        else:
            req = urllib.request.Request(full_url, headers={"User-Agent": "OIBSIP-WeatherApp/1.0"})
            with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
                status_code = resp.status
                raw_bytes = resp.read()
                payload = json.loads(raw_bytes.decode("utf-8"))

        if status_code == 200:
            return parse_weather_payload(payload, is_demo=False)
        elif status_code == 404:
            raise LookupError(f"City '{cleaned_query}' not found. Please verify spelling.")
        elif status_code == 401:
            raise PermissionError(
                "Invalid or inactive OpenWeatherMap API key. "
                "(Note: Free tier keys can take 1-2 hours to activate after creation)."
            )
        else:
            message = payload.get("message", f"HTTP Status {status_code}")
            raise ConnectionError(f"Weather API error: {message}")

    except (urllib.error.HTTPError,) as http_err:
        if http_err.code == 404:
            raise LookupError(f"City '{cleaned_query}' not found. Please verify spelling.")
        elif http_err.code == 401:
            raise PermissionError("Invalid or inactive OpenWeatherMap API key.")
        else:
            raise ConnectionError(f"HTTP request error: {http_err.code} {http_err.reason}")

    except (urllib.error.URLError, TimeoutError) as net_err:
        raise ConnectionError(
            f"Network error: Unable to connect to weather service. Details: {net_err}"
        )


# =====================================================================
# CLI (Command-Line Interface) Presentation
# =====================================================================

def display_cli_banner() -> None:
    """Displays styled welcome banner."""
    border = "=" * 66
    print("\n" + border)
    print("      OASIS INFOBYTE PYTHON INTERNSHIP - TASK 4")
    print("                 LIVE WEATHER FORECAST APP")
    print(border)
    print("  Real-time meteorological monitoring powered by OpenWeatherMap API.")
    print(border + "\n")


def print_weather_card(report: WeatherReport) -> None:
    """Displays formatted terminal card for weather conditions."""
    border = "-" * 66
    icon = WEATHER_ICONS.get(report.condition, "🌤️")

    print("\n" + border)
    header_status = " [DEMO METEOROLOGY DATA]" if report.is_demo else " [LIVE API DATA]"
    print(f"   WEATHER REPORT FOR {report.city_name.upper()}, {report.country}{header_status}")
    print(border)
    print(f"   Condition           : {icon}  {report.condition} ({report.description})")
    print(f"   Temperature         : {report.temp_c}°C  /  {report.temp_f}°F")
    print(f"   Feels Like          : {report.feels_like_c}°C  /  {report.feels_like_f}°F")
    print(f"   Humidity            : {report.humidity}%")
    print(f"   Wind Speed          : {report.wind_speed_kmh} km/h  ({report.wind_speed_mps} m/s / {report.wind_speed_mph} mph)")
    print(f"   Atmospheric Pressure: {report.pressure_hpa} hPa")
    print(f"   Visibility          : {report.visibility_km} km")
    print(f"   Recorded At         : {report.timestamp}")
    print(border + "\n")


def run_cli_interactive(api_key: Optional[str] = None, use_demo: bool = False) -> None:
    """Runs interactive command-line session."""
    display_cli_banner()

    resolved_key = api_key or os.getenv(ENV_API_KEY_NAME, "")
    if not resolved_key and not use_demo:
        print("  [INFO] No API key detected. Running in Demo / Offline Fallback Mode.")
        print(f"         Set the {ENV_API_KEY_NAME} environment variable for live data.\n")
        use_demo = True

    while True:
        try:
            city = input("Enter city name or postal code (or 'q' to quit): ").strip()
            if not city:
                print("  [!] Please enter a valid city name.")
                continue

            if city.lower() in ("q", "quit", "exit"):
                print("\nThank you for using the Weather App. Have a wonderful day!\n")
                break

            print(f"  --> Fetching meteorological data for '{city}'...")
            report = fetch_weather(query=city, api_key=resolved_key, use_demo=use_demo)
            print_weather_card(report)

        except (LookupError, PermissionError, ConnectionError, ValueError) as err:
            print(f"  [ERROR] {err}\n")
        except (KeyboardInterrupt, EOFError):
            print("\n\nOperation canceled. Exiting.\n")
            break


# =====================================================================
# Modern Tkinter Graphical User Interface (GUI)
# =====================================================================

def launch_gui(api_key: Optional[str] = None, use_demo: bool = False) -> None:
    """Launches modern desktop Tkinter GUI."""
    try:
        import tkinter as tk
        from tkinter import messagebox, ttk
    except ImportError as e:
        print(f"[ERROR] Tkinter is not available in this environment: {e}")
        return

    root = tk.Tk()
    root.title("Oasis Infobyte - Weather App")
    root.geometry("560x700")
    root.minsize(500, 640)

    # Theme & Colors
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    BG_COLOR = "#ECEFF1"
    PRIMARY_COLOR = "#0D47A1"  # Deep weather blue
    CARD_BG = "#FFFFFF"
    TEXT_MUTED = "#546E7A"

    root.configure(bg=BG_COLOR)

    # State variables
    unit_var = tk.StringVar(value="C")
    demo_mode_var = tk.BooleanVar(value=use_demo or not (api_key or os.getenv(ENV_API_KEY_NAME)))
    current_report_holder = {"report": None}

    # Header Frame
    header_frame = tk.Frame(root, bg=PRIMARY_COLOR, pady=16)
    header_frame.pack(fill=tk.X)

    title_lbl = tk.Label(
        header_frame,
        text="🌤️ LIVE WEATHER FORECAST",
        font=("Segoe UI", 16, "bold"),
        fg="#FFFFFF",
        bg=PRIMARY_COLOR,
    )
    title_lbl.pack()

    subtitle_lbl = tk.Label(
        header_frame,
        text="Oasis Infobyte Internship - Task 4",
        font=("Segoe UI", 9),
        fg="#BBDEFB",
        bg=PRIMARY_COLOR,
    )
    subtitle_lbl.pack(pady=(2, 0))

    # Main content container
    content = tk.Frame(root, bg=BG_COLOR, padx=22, pady=14)
    content.pack(fill=tk.BOTH, expand=True)

    # Search Bar Frame
    search_frame = tk.LabelFrame(
        content,
        text="  Search City or Postal Code  ",
        font=("Segoe UI", 10, "bold"),
        bg=CARD_BG,
        fg="#263238",
        padx=14,
        pady=12,
        relief=tk.GROOVE,
    )
    search_frame.pack(fill=tk.X, pady=(0, 12))

    entry_city = ttk.Entry(search_frame, font=("Segoe UI", 11))
    entry_city.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    entry_city.insert(0, "Chennai")
    entry_city.focus()

    # Options Bar Frame
    options_frame = tk.Frame(search_frame, bg=CARD_BG)
    options_frame.pack(side=tk.RIGHT)

    btn_search = tk.Button(
        options_frame,
        text="🔍 Search",
        font=("Segoe UI", 10, "bold"),
        bg=PRIMARY_COLOR,
        fg="#FFFFFF",
        activebackground="#1565C0",
        activeforeground="#FFFFFF",
        padx=14,
        pady=4,
        relief=tk.FLAT,
        cursor="hand2",
    )
    btn_search.pack(side=tk.LEFT)

    # Unit selector radio buttons & Demo toggle
    sub_options = tk.Frame(content, bg=BG_COLOR)
    sub_options.pack(fill=tk.X, pady=(0, 10))

    chk_demo = tk.Checkbutton(
        sub_options,
        text="Demo / Offline Mode",
        variable=demo_mode_var,
        bg=BG_COLOR,
        font=("Segoe UI", 9),
    )
    chk_demo.pack(side=tk.LEFT)

    unit_lbl = tk.Label(sub_options, text="Units:", font=("Segoe UI", 9, "bold"), bg=BG_COLOR)
    unit_lbl.pack(side=tk.RIGHT, padx=(6, 2))

    r_f = tk.Radiobutton(
        sub_options, text="°F", variable=unit_var, value="F", bg=BG_COLOR, font=("Segoe UI", 9)
    )
    r_f.pack(side=tk.RIGHT)

    r_c = tk.Radiobutton(
        sub_options, text="°C", variable=unit_var, value="C", bg=BG_COLOR, font=("Segoe UI", 9)
    )
    r_c.pack(side=tk.RIGHT)

    # Weather Display Card
    card_frame = tk.LabelFrame(
        content,
        text="  Current Weather Assessment  ",
        font=("Segoe UI", 10, "bold"),
        bg=CARD_BG,
        fg="#263238",
        padx=18,
        pady=14,
        relief=tk.GROOVE,
    )
    card_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    lbl_city_country = tk.Label(
        card_frame,
        text="--",
        font=("Segoe UI", 18, "bold"),
        fg="#263238",
        bg=CARD_BG,
    )
    lbl_city_country.pack(anchor="center", pady=(4, 0))

    lbl_weather_icon = tk.Label(
        card_frame,
        text="⛅",
        font=("Segoe UI", 48),
        bg=CARD_BG,
    )
    lbl_weather_icon.pack(anchor="center", pady=(0, 2))

    lbl_temperature = tk.Label(
        card_frame,
        text="--°",
        font=("Segoe UI", 32, "bold"),
        fg=PRIMARY_COLOR,
        bg=CARD_BG,
    )
    lbl_temperature.pack(anchor="center")

    lbl_description = tk.Label(
        card_frame,
        text="Enter a city and click 'Search'",
        font=("Segoe UI", 11, "italic"),
        fg=TEXT_MUTED,
        bg=CARD_BG,
    )
    lbl_description.pack(anchor="center", pady=(0, 10))

    # Metric details grid inside card
    grid_frame = tk.Frame(card_frame, bg=CARD_BG)
    grid_frame.pack(fill=tk.X, pady=(10, 0))

    # Column 0: Humidity & Wind
    lbl_humidity_val = tk.Label(grid_frame, text="💧 Humidity: --", font=("Segoe UI", 10), bg=CARD_BG)
    lbl_humidity_val.grid(row=0, column=0, sticky="w", padx=20, pady=4)

    lbl_wind_val = tk.Label(grid_frame, text="💨 Wind: --", font=("Segoe UI", 10), bg=CARD_BG)
    lbl_wind_val.grid(row=1, column=0, sticky="w", padx=20, pady=4)

    # Column 1: Feels Like & Pressure
    lbl_feels_val = tk.Label(grid_frame, text="🌡️ Feels Like: --", font=("Segoe UI", 10), bg=CARD_BG)
    lbl_feels_val.grid(row=0, column=1, sticky="w", padx=20, pady=4)

    lbl_pressure_val = tk.Label(grid_frame, text="🧭 Pressure: --", font=("Segoe UI", 10), bg=CARD_BG)
    lbl_pressure_val.grid(row=1, column=1, sticky="w", padx=20, pady=4)

    # Status Bar
    status_lbl = tk.Label(
        content,
        text="Ready. Enter a city name to search.",
        font=("Segoe UI", 8),
        fg=TEXT_MUTED,
        bg=BG_COLOR,
        anchor="w",
    )
    status_lbl.pack(fill=tk.X, side=tk.BOTTOM)

    # GUI Update Handler
    def refresh_display():
        rep: Optional[WeatherReport] = current_report_holder["report"]
        if not rep:
            return

        is_c = unit_var.get() == "C"
        temp_str = f"{rep.temp_c}°C" if is_c else f"{rep.temp_f}°F"
        feels_str = f"{rep.feels_like_c}°C" if is_c else f"{rep.feels_like_f}°F"
        wind_str = f"{rep.wind_speed_kmh} km/h" if is_c else f"{rep.wind_speed_mph} mph"

        lbl_city_country.config(text=f"{rep.city_name}, {rep.country}")
        lbl_weather_icon.config(text=WEATHER_ICONS.get(rep.condition, "🌤️"))
        lbl_temperature.config(text=temp_str)
        lbl_description.config(text=f"{rep.description}")

        lbl_humidity_val.config(text=f"💧 Humidity: {rep.humidity}%")
        lbl_wind_val.config(text=f"💨 Wind Speed: {wind_str}")
        lbl_feels_val.config(text=f"🌡️ Feels Like: {feels_str}")
        lbl_pressure_val.config(text=f"🧭 Pressure: {rep.pressure_hpa} hPa")

        source_text = "Demo Mode (Mock data)" if rep.is_demo else "Live OpenWeatherMap API"
        status_lbl.config(text=f"Last updated: {rep.timestamp} | Source: {source_text}")

    def on_search():
        query = entry_city.get().strip()
        if not query:
            messagebox.showwarning("Input Required", "Please enter a city name or postal code.")
            return

        status_lbl.config(text=f"Querying weather for '{query}'...")
        root.update_idletasks()

        try:
            report = fetch_weather(
                query=query,
                api_key=api_key,
                use_demo=demo_mode_var.get(),
            )
            current_report_holder["report"] = report
            refresh_display()
        except LookupError as err:
            messagebox.showerror("Location Not Found", str(err))
            status_lbl.config(text=f"Error: {err}")
        except PermissionError as err:
            messagebox.showwarning("API Key Issue", f"{err}\n\nToggling to Demo Mode.")
            demo_mode_var.set(True)
            on_search()
        except Exception as err:
            messagebox.showerror("Error", str(err))
            status_lbl.config(text=f"Error: {err}")

    # Bind events
    btn_search.config(command=on_search)
    root.bind("<Return>", lambda e: on_search())
    unit_var.trace_add("write", lambda *args: refresh_display())

    # Initial search on startup
    on_search()

    # Center window
    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()


# =====================================================================
# Main Application Dispatcher
# =====================================================================

def parse_cli_args() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Oasis Infobyte Task 4: Advanced Weather App (CLI & GUI)"
    )
    parser.add_argument("--gui", action="store_true", help="Launch Tkinter Graphical User Interface.")
    parser.add_argument("--cli", action="store_true", help="Launch interactive Command-Line Interface.")
    parser.add_argument("-c", "--city", type=str, help="Quick one-shot weather lookup for a city.")
    parser.add_argument("--api-key", type=str, help="OpenWeatherMap API Key.")
    parser.add_argument("--demo", action="store_true", help="Force offline mock demo mode.")
    return parser.parse_args()


def main() -> None:
    """Entry point dispatching CLI or GUI."""
    args = parse_cli_args()

    # One-shot command line lookup
    if args.city:
        try:
            report = fetch_weather(
                query=args.city,
                api_key=args.api_key,
                use_demo=args.demo,
            )
            print_weather_card(report)
            sys.exit(0)
        except Exception as err:
            print(f"[ERROR] {err}", file=sys.stderr)
            sys.exit(1)

    if args.gui:
        launch_gui(api_key=args.api_key, use_demo=args.demo)
    elif args.cli:
        run_cli_interactive(api_key=args.api_key, use_demo=args.demo)
    else:
        # Default prompt
        display_cli_banner()
        print("Choose an option:")
        print("  [1] Interactive Terminal CLI")
        print("  [2] Graphical Desktop UI (Tkinter)")
        print("  [3] Exit Application")

        try:
            choice = input("\nSelect (1-3) [1]: ").strip()
            if choice == "2":
                launch_gui(api_key=args.api_key, use_demo=args.demo)
            elif choice in ("3", "q", "quit", "exit"):
                print("\nGoodbye!\n")
            else:
                run_cli_interactive(api_key=args.api_key, use_demo=args.demo)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.\n")


if __name__ == "__main__":
    main()
