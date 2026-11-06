# Oasis Infobyte Internship (OIBSIP) - Task 3: Random Password Generator

> **Domain:** Python Development  
> **Task Name:** Random Password Generator (Task 3)  
> **Level:** Beginner / Advanced  
> **Author:** Silambarasan

---

## 📌 Project Objective

The primary objective of this project is to develop a robust, cryptographically secure command-line tool that generates high-entropy, customizable passwords tailored to user-specified rules. 

Passwords protect sensitive digital identities; this project addresses security vulnerabilities by employing Python's `secrets` module (Cryptographically Secure Pseudo-Random Number Generator — CSPRNG) rather than standard deterministic pseudo-random generators, ensuring compliance with modern security and password-policy guidelines.

---

## ✨ Features

- **Enforced Security Standards:** Enforces a minimum length of 8 characters (up to 128) to prevent weak passwords.
- **Granular Customization:** Allows toggleable selection of:
  - Uppercase letters (`A-Z`)
  - Lowercase letters (`a-z`)
  - Numbers (`0-9`)
  - Special symbols / punctuation (`!@#$%^&*...`)
- **Guaranteed Category Representation:** Ensures at least one character from every user-selected character type is included.
- **Cryptographic Shuffling:** Leverages `secrets.SystemRandom().shuffle()` to eliminate predictable token positions.
- **Password Strength Assessment:** Displays an automated strength rating (Weak, Moderate, Strong, Very Strong) based on entropy parameters.
- **Comprehensive Input Validation:** Gracefully handles invalid numeric lengths, non-integer inputs, out-of-range bounds, and zero-selection errors.
- **Interactive Session Loop:** Enables consecutive password generation without needing to restart the script.
- **Unit Tested:** Includes an automated test suite (`test_password_generator.py`) verifying constraints and security properties.

---

## 🛠️ Tech Stack & Standard Libraries

This project uses Python's standard library with zero external dependencies required:

| Component | Library / Module | Purpose |
|---|---|---|
| **Language** | Python 3.8+ | Core application runtime |
| **CSPRNG Source** | `secrets` | Cryptographically secure randomness for tokens and selections |
| **Character Sets** | `string` | Safe, locale-independent character constants (`ascii_letters`, `digits`, `punctuation`) |
| **System Interface** | `sys` | Terminal interaction handling and clean exit controls |
| **Type Hints** | `typing` | Static type annotations for clean, readable code |
| **Automated Testing** | `unittest` | Regression verification and policy assertion |

> **Why `secrets` over `random`?**  
> Python's standard `random` module uses the Mersenne Twister engine, which is completely deterministic and predictable if internal state is observed. The `secrets` module leverages the operating system's cryptographic random source (`/dev/urandom` on POSIX, `CryptGenRandom`/`BCryptGenRandom` on Windows), ensuring passwords cannot be predicted by an adversary.

---

## 📂 Oasis Infobyte Repository Structure

To submit this project to your GitHub repository under the official Oasis Infobyte folder layout:

```text
OIBSIP/
└── Python-Task3-PasswordGenerator/
    ├── main.py                     # Main CLI application script
    ├── test_password_generator.py  # Automated unit test suite
    └── README.md                   # Project documentation & execution guide
```

---

## 🚀 How to Run the Application

### 1. Prerequisites
Ensure Python 3.8 or higher is installed:
```bash
python --version
```

### 2. Clone or Navigate to the Directory
```bash
git clone https://github.com/<your-username>/OIBSIP.git
cd OIBSIP/Python-Task3-PasswordGenerator
```

### 3. Run the Password Generator
Execute the main script using the Python interpreter:
```bash
python main.py
```

### 4. Run the Test Suite (Optional)
Run the automated test suite to verify all validation and generation logic:
```bash
python -m unittest test_password_generator.py -v
```

---

## 🖥️ Sample CLI Output

```text
================================================================
   OASIS INFOBYTE PYTHON INTERNSHIP - TASK 3
        CRYPTOGRAPHIC RANDOM PASSWORD GENERATOR
================================================================
  Generate strong, unpredictable, and customizable passwords
  powered by Python's 'secrets' module (CSPRNG).


Enter desired password length (min 8, max 128) [default 16]: 16

Select character types to include:
  Include Uppercase letters (A-Z)? [Y/n]: y
  Include Lowercase letters (a-z)? [Y/n]: y
  Include Numbers (0-9)? [Y/n]: y
  Include Special symbols (!@#$%...)? [Y/n]: y

----------------------------------------------------------------
  GENERATED PASSWORD:
  --> k9#Wb&v2Q$8mZ!pL
----------------------------------------------------------------
  Length        : 16 characters
  Strength Level: Very Strong
  Assessment    : Excellent entropy. Resistant to brute-force and dictionary attacks.
----------------------------------------------------------------

Would you like to generate another password? [Y/n]: n

Thank you for using the Random Password Generator. Goodbye!
```

---

## 🛡️ Edge Cases Handled

1. **Length < 8:** Rejects length and displays a warning, prompting re-entry.
2. **Non-Integer Length:** Catches `ValueError` and politely asks for a positive integer.
3. **No Character Types Selected:** Catches zero selection error and prompts the user to select at least one type.
4. **Clean Exit:** Handles `Ctrl+C` (`KeyboardInterrupt`) and `EOF` gracefully without raw traceback dumps.

---

## 📜 License
This project is submitted as part of the **Oasis Infobyte Internship Program (OIBSIP)** for educational and assessment purposes.

