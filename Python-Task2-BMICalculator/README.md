# Oasis Infobyte Internship (OIBSIP) - Task 2: BMI Calculator

> **Domain:** Python Development  
> **Task Name:** Body Mass Index (BMI) Calculator (Task 2)  
> **Level:** Beginner / Advanced  
> **Author:** Silambarasan  

---

## 📌 Project Objective

The primary objective of this project is to develop a reliable, production-ready **Body Mass Index (BMI) Calculator** that provides users with fast, accurate health categorization based on World Health Organization (WHO) standards.

Body Mass Index is a widely used screening metric to assess whether an individual has a healthy body weight for their height. This application combines mathematical precision with strict validation safeguards, offering both an **interactive Command-Line Interface (CLI)** and an intuitive **Graphical User Interface (GUI)** built with Tkinter.

---

## ✨ Key Features

- **Standard Metric Formula:** Computes BMI using the internationally recognized formula:  
  $$\text{BMI} = \frac{\text{Weight (kg)}}{\text{Height (m)}^2}$$
- **Official WHO Health Classifications:** Accurately groups results into:
  - **Underweight:** $\text{BMI} < 18.5$
  - **Normal weight:** $18.5 \le \text{BMI} \le 24.9$
  - **Overweight:** $25.0 \le \text{BMI} \le 29.9$
  - **Obese:** $\text{BMI} \ge 30.0$
- **Ideal Healthy Weight Range Estimation:** Automatically computes and displays the target healthy weight range (corresponding to normal BMI 18.5–24.9) specifically tailored to the user's height.
- **Robust Defensive Validation:**
  - Rejects non-numeric, alphabetic, or empty inputs.
  - Rejects zero and negative values for weight and height.
  - Enforces physiological biological boundary constraints ($1.0\text{ kg} \le \text{weight} \le 650.0\text{ kg}$ and $0.40\text{ m} \le \text{height} \le 2.80\text{ m}$).
  - Automatically identifies whether height was entered in meters (e.g., `1.75`) or centimeters (e.g., `175`) with smart conversion.
- **Dual Mode (CLI & Modern Tkinter GUI):**
  - **CLI Mode:** Richly formatted terminal summary cards, WHO chart reference table, and continuous session loop.
  - **Tkinter GUI:** Clean card layout, color-coded severity badges, input reset, and keyboard shortcut (`Enter` to calculate).
- **Automated Unit Test Suite:** Includes 29 comprehensive unit tests written with Python's built-in `unittest` framework.

---

## 📐 Mathematical Formulation & Reference Table

| Category | BMI Range ($\text{kg/m}^2$) | Health Risk Assessment | Color Indicator |
|---|---|---|---|
| **Underweight** | $< 18.5$ | Increased risk of nutritional deficiency & osteoporosis | Blue (`#1E88E5`) |
| **Normal** | $18.5 - 24.9$ | Optimal health; lowest statistical risk of chronic illness | Green (`#2E7D32`) |
| **Overweight** | $25.0 - 29.9$ | Moderate risk; diet and exercise modifications recommended | Orange (`#EF6C00`) |
| **Obese** | $\ge 30.0$ | High clinical risk (cardiovascular, diabetes, hypertension) | Red (`#C62828`) |

---

## 🛠️ Tech Stack & Standard Libraries

This project uses Python's standard library with **zero external dependencies** required:

| Component | Library / Module | Purpose |
|---|---|---|
| **Language** | Python 3.8+ | Core application runtime |
| **GUI Framework** | `tkinter` & `ttk` | Graphical User Interface with styled widgets and dynamic cards |
| **CLI Argument Parsing** | `argparse` | Command-line flags (`--cli`, `--gui`, `-w`, `-H`) |
| **System Interface** | `sys` | Clean exit codes, standard stream error formatting |
| **Type Hints** | `typing` | Static type annotations (`Tuple`, `Optional`) for clean code maintainability |
| **Automated Testing** | `unittest` | Comprehensive test assertions covering calculations, boundaries, and validation |

---

## 📂 Oasis Infobyte Repository Structure

The project follows the official Oasis Infobyte folder layout:

```text
OIBSIP/
├── Python-Task2-BMICalculator/
│   ├── main.py                     # Main application (Dual Mode: CLI & Tkinter GUI)
│   ├── test_bmi_calculator.py      # Automated unit test suite (29 tests)
│   ├── .gitignore                  # Git ignore rules for Python artifacts
│   └── README.md                   # Comprehensive documentation & execution guide
└── Python-Task3-PasswordGenerator/
```

---

## 🚀 How to Run the Application

### 1. Prerequisites
Ensure Python 3.8 or higher is installed:
```bash
python --version
```

### 2. Navigate to the Task Directory
```bash
cd OIBSIP/Python-Task2-BMICalculator
```

### 3. Launching the Application

#### A. Interactive Menu (Default)
Run without flags to open the interactive menu allowing you to choose between CLI, GUI, or reference tables:
```bash
python main.py
```

#### B. Direct Graphical GUI Mode (Tkinter)
Launch the modern desktop application directly:
```bash
python main.py --gui
```

#### C. Direct CLI Mode
Jump straight into the command-line prompts:
```bash
python main.py --cli
```

#### D. Fast One-Shot Command Line Calculation
Quickly calculate BMI without navigating prompts:
```bash
# Syntax: python main.py -w <weight_in_kg> -H <height_in_meters>
python main.py -w 70 -H 1.75
```

### 4. Running the Automated Unit Tests
Execute the unit test suite with verbose output:
```bash
python -m unittest test_bmi_calculator.py -v
```

Or run test discovery from the root of the repository:
```bash
python -m unittest discover -s Python-Task2-BMICalculator -v
```

---

## 🖥️ Sample CLI Output

```text
==================================================================
      OASIS INFOBYTE PYTHON INTERNSHIP - TASK 2
               BODY MASS INDEX (BMI) CALCULATOR
==================================================================
  Accurately assess your body mass index, WHO classification,
  and ideal healthy weight range with precision.
==================================================================

Please enter your measurements below:
   Enter your weight in kilograms (kg): 72
   Enter your height (in meters e.g. 1.75, or cm e.g. 175): 1.78

------------------------------------------------------------------
                    BMI ASSESSMENT REPORT
------------------------------------------------------------------
   User Weight         : 72.00 kg
   User Height         : 1.78 m (178.0 cm)
   Calculated BMI      : 22.72 kg/m²
   Classification      : [NORMAL]
   Healthy Weight Span : 58.6 kg - 78.9 kg (for your height)
------------------------------------------------------------------
   Health Guidance:
   --> Congratulations! Your BMI is within the healthy weight range. Maintain your current balanced diet and regular physical activity.
------------------------------------------------------------------
```

---

## 🧪 Unit Test Coverage

The test suite in [`test_bmi_calculator.py`](file:///d:/Silambu/OIBSIP/Python-Task2-BMICalculator/test_bmi_calculator.py) provides 100% test coverage for:
1. **Mathematical Accuracy:** Formula precision and rounding up to two decimal places.
2. **Boundary Transition Verification:** Exact threshold boundaries between Underweight/Normal (`18.49` vs `18.5`), Normal/Overweight (`24.99` vs `25.0`), and Overweight/Obese (`29.99` vs `30.0`).
3. **Defensive Validation:** Non-positive inputs, zero height, negative weight, invalid types, and non-physiological extremes.
4. **Target Weight Range Estimation:** Accurate calculation of the healthy weight window.

---

## 📄 License
This project is developed as part of the **Oasis Infobyte Python Programming Internship (OIBSIP)**. Open-source and free to use for educational and assessment purposes.

