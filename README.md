# Oasis Infobyte Internship (OIBSIP) - Python Development

Welcome to the **Oasis Infobyte Internship (OIBSIP)** Python Programming repository. This repository showcases production-grade, cleanly structured, and thoroughly tested Python applications developed during the internship.

---

## 👨‍💻 Intern Details

- **Intern Name:** Silambarasan
- **Domain:** Python Development
- **Internship Program:** Oasis Infobyte Internship (OIBSIP)

---

## 📁 Repository Structure & Tasks Overview

```text
OIBSIP/
├── Python-Task2-BMICalculator/
│   ├── main.py                     # Dual-mode BMI calculator (CLI & Tkinter GUI)
│   ├── test_bmi_calculator.py      # Automated unit tests (29 tests)
│   ├── .gitignore                  # Git ignore rules
│   └── README.md                   # Detailed Task 2 documentation
│
├── Python-Task3-PasswordGenerator/
│   ├── main.py                     # Cryptographic random password generator
│   ├── test_password_generator.py  # Automated unit tests
│   ├── .gitignore                  # Git ignore rules
│   └── README.md                   # Detailed Task 3 documentation
│
└── Python-Task4-WeatherApp/
    ├── main.py                     # Dual-mode Weather application (CLI & Tkinter GUI)
    ├── test_weather_app.py         # Automated unit tests (17 tests)
    ├── .gitignore                  # Git ignore rules
    └── README.md                   # Detailed Task 4 documentation
```

---

## 📋 Task Summaries

### 🏋️ [Task 2: BMI Calculator (Body Mass Index)](file:///d:/Silambu/OIBSIP/Python-Task2-BMICalculator/README.md)
A Body Mass Index calculator with medical classification, biological range validation, ideal weight span calculation, and dual-mode interface (interactive CLI and modern Tkinter desktop GUI).
- **Formula:** $\text{BMI} = \frac{\text{Weight (kg)}}{\text{Height (m)}^2}$
- **Standards:** World Health Organization (WHO) categories (Underweight, Normal, Overweight, Obese).
- **Interface:** Interactive terminal CLI loop & Tkinter graphical desktop UI.
- **Testing:** 29 automated unit tests with `unittest`.

### 🔐 [Task 3: Random Password Generator](file:///d:/Silambu/OIBSIP/Python-Task3-PasswordGenerator/README.md)
A cryptographically secure, customizable random password generator using Python's standard library `secrets` module (CSPRNG).
- **Security:** CSPRNG via OS entropy source, guaranteed character category representation, and cryptographic shuffle.
- **Customization:** Toggle uppercase, lowercase, numbers, and special symbols; customizable length (8–128).
- **Features:** Automated entropy and password strength scoring.
- **Testing:** Comprehensive unit test suite with `unittest`.

### 🌤️ [Task 4: Basic Weather App](file:///d:/Silambu/OIBSIP/Python-Task4-WeatherApp/README.md)
A live meteorological monitoring application integrated with the OpenWeatherMap API, featuring automatic metric/imperial conversion, error recovery, offline demonstration fallback, and a modern Tkinter GUI.
- **API Source:** OpenWeatherMap REST API + built-in offline simulation dataset.
- **Metrics:** Current temperature (°C/°F), humidity (%), weather conditions, wind speed (km/h & mph), pressure, visibility.
- **Interface:** Interactive terminal CLI & Tkinter desktop graphical application.
- **Testing:** 17 automated unit tests with `unittest`.

---

## 🚀 Running the Projects

### Task 2: BMI Calculator
```bash
cd Python-Task2-BMICalculator

# Interactive CLI mode
python main.py

# Modern Tkinter GUI mode
python main.py --gui

# Run unit tests
python -m unittest test_bmi_calculator.py -v
```

### Task 3: Random Password Generator
```bash
cd Python-Task3-PasswordGenerator

# Run generator
python main.py

# Run unit tests
python -m unittest test_password_generator.py -v
```

### Task 4: Weather App
```bash
cd Python-Task4-WeatherApp

# Interactive CLI mode
python main.py

# Modern Tkinter GUI mode
python main.py --gui

# Run in offline demo mode
python main.py -c "Chennai" --demo

# Run unit tests
python -m unittest test_weather_app.py -v
```

---

## 📜 License & Acknowledgments
Developed with standard Python libraries as part of the **Oasis Infobyte Python Programming Internship (OIBSIP)**.
