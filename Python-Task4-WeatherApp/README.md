# Oasis Infobyte Internship (OIBSIP) - Task 4: Weather App

> **Domain:** Python Development  
> **Task Name:** Basic Weather App (Task 4)  
> **Level:** Beginner / Advanced  
> **Author:** Silambarasan  

---

## 📌 Project Objective

The primary objective of this project is to develop a production-ready, feature-complete **Weather Application** that delivers real-time meteorological conditions for any city or postal code worldwide using the **OpenWeatherMap REST API**.

The application supports both an **interactive terminal interface (CLI)** and a **graphical user interface (Tkinter GUI)**, along with automatic temperature conversions (°C and °F), wind speed metrics, humidity ratings, atmospheric pressure, and an intelligent offline fallback mode for smooth demonstration without waiting for API key provisioning.

---

## ✨ Key Features

- **Live Weather Data Integration:** Queries the OpenWeatherMap API for live temperature, weather conditions, humidity percentage, wind speed, pressure, and visibility.
- **Dual Interface Modes:**
  - **Tkinter GUI:** Desktop application featuring dynamic weather icons, live search bar, instant °C/°F unit toggling, and clean visual cards.
  - **Interactive CLI:** Terminal dashboard with structured ASCII cards, input prompts, and continuous query session loops.
- **Dual Temperature & Wind Metric Support:**
  - Temperatures rendered in both **Celsius (°C)** and **Fahrenheit (°F)** with feels-like calculations.
  - Wind speed displayed in both **km/h**, **m/s**, and **mph**.
- **Defensive Error Handling:**
  - Gracefully captures invalid/empty search terms.
  - Handles HTTP 404 (City Not Found) with actionable suggestions.
  - Handles HTTP 401 (Unauthorized / Inactive API Key) without crashing.
  - Catches network timeouts, DNS resolution failures, and connection drops.
- **Built-in Offline / Demonstration Fallback:**
  - Includes a curated offline meteorological dataset for major cities (Chennai, Delhi, Mumbai, Bengaluru, London, New York, Tokyo, Paris).
  - Enables instant evaluation and testing even in network-isolated environments or prior to API key activation.
- **Automated Unit Testing:** Full coverage test suite with 17 unit tests verifying parsing, mathematical conversions, error handling, and mock API network interactions.

---

## 🛠️ Tech Stack & Dependencies

| Component | Library / Module | Purpose |
|---|---|---|
| **Language** | Python 3.8+ | Core runtime |
| **HTTP Client** | `requests` / `urllib.request` | Communicates with OpenWeatherMap REST API endpoints |
| **GUI Framework** | `tkinter` & `ttk` | Modern desktop graphical user interface |
| **Command Line Interface** | `argparse` | CLI flags (`--gui`, `--cli`, `-c`, `--demo`, `--api-key`) |
| **Automated Testing** | `unittest` & `unittest.mock` | Unit tests and network payload simulation |
| **Data Architecture** | `dataclasses` & `json` | Structured, type-safe data modeling and parsing |

---

## 🔑 How to Obtain a Free OpenWeatherMap API Key

1. Visit [OpenWeatherMap Sign Up](https://home.openweathermap.org/users/sign_up) and create a free account.
2. Navigate to your profile's **API Keys** section: [https://home.openweathermap.org/api_keys](https://home.openweathermap.org/api_keys).
3. Copy your default 32-character API key (or generate a new named key).
4. Set it as an environment variable or pass it to the app:

**On Windows (PowerShell):**
```powershell
$env:OPENWEATHER_API_KEY="your_api_key_here"
```

**On Linux / macOS:**
```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

> **Note on Free Tier Activation:** Newly generated OpenWeatherMap keys typically require 1 to 2 hours to activate across global CDN servers. If your key is pending activation, the app will offer to run in **Demo / Offline Mode** automatically.

---

## 📂 Oasis Infobyte Repository Structure

```text
OIBSIP/
├── Python-Task2-BMICalculator/
│   ├── main.py
│   ├── test_bmi_calculator.py
│   ├── .gitignore
│   └── README.md
├── Python-Task3-PasswordGenerator/
│   ├── main.py
│   ├── test_password_generator.py
│   ├── .gitignore
│   └── README.md
├── Python-Task4-WeatherApp/
│   ├── main.py                     # Main application (Dual Mode: CLI & Tkinter GUI)
│   ├── test_weather_app.py         # Automated unit test suite (17 tests)
│   ├── .gitignore                  # Git ignore rules
│   └── README.md                   # Comprehensive Task 4 documentation
├── .gitignore                      # Root ignore rules
└── README.md                       # Master portfolio overview
```

---

## 🚀 How to Run the Application

### 1. Navigate to the Task Directory
```bash
cd OIBSIP/Python-Task4-WeatherApp
```

### 2. Launching the Application

#### A. Interactive Menu (Default)
```bash
python main.py
```

#### B. Launch Desktop Graphical GUI (Tkinter)
```bash
python main.py --gui
```

#### C. Launch Interactive Terminal CLI
```bash
python main.py --cli
```

#### D. Fast One-Shot Command Line Query
```bash
# Query any city in live mode:
python main.py -c "London"

# Or query in offline demo mode:
python main.py -c "Chennai" --demo
```

### 3. Running the Automated Unit Tests
Run the test suite directly:
```bash
python -m unittest test_weather_app.py -v
```

Or run via test discovery from the repository root:
```bash
python -m unittest discover -s Python-Task4-WeatherApp -v
```

---

## 🖥️ Sample CLI Output

```text
==================================================================
      OASIS INFOBYTE PYTHON INTERNSHIP - TASK 4
                 LIVE WEATHER FORECAST APP
==================================================================
  Real-time meteorological monitoring powered by OpenWeatherMap API.
==================================================================

Enter city name or postal code: Chennai
  --> Fetching meteorological data for 'Chennai'...

------------------------------------------------------------------
   WEATHER REPORT FOR CHENNAI, IN [LIVE API DATA]
------------------------------------------------------------------
   Condition           : ☁️  Clouds (Scattered clouds)
   Temperature         : 31.4°C  /  88.52°F
   Feels Like          : 36.2°C  /  97.16°F
   Humidity            : 78%
   Wind Speed          : 14.76 km/h  (4.1 m/s / 9.17 mph)
   Atmospheric Pressure: 1012 hPa
   Visibility          : 9.0 km
   Recorded At         : 2026-11-06 12:30:15
------------------------------------------------------------------
```

---

## 📄 License
Developed as part of the **Oasis Infobyte Python Programming Internship (OIBSIP)**. Open-source and free to use for educational and assessment purposes.
