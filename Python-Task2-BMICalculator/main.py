"""
Oasis Infobyte Internship - Python Development
Task 2: BMI Calculator (Body Mass Index)
Author: Silambarasan (OIBSIP Intern)
Description: A robust, production-grade Body Mass Index (BMI) calculator
             featuring comprehensive input validation, medical categorization,
             ideal weight range estimation, interactive CLI mode, and a modern
             Tkinter Graphical User Interface (GUI).
"""

import argparse
import sys
from typing import Optional, Tuple

# Physical boundary constants for realistic biological validation
MIN_WEIGHT_KG = 1.0       # Minimum plausible weight (kg)
MAX_WEIGHT_KG = 650.0     # Maximum plausible weight (kg)
MIN_HEIGHT_M = 0.40       # Minimum plausible adult/child height (meters)
MAX_HEIGHT_M = 2.80       # Maximum plausible human height (meters)

# Standard WHO BMI thresholds
BMI_UNDERWEIGHT_MAX = 18.5
BMI_NORMAL_MAX = 25.0     # 18.5 to < 25.0 is Normal
BMI_OVERWEIGHT_MAX = 30.0 # 25.0 to < 30.0 is Overweight


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculates Body Mass Index (BMI) using the standard formula:
        BMI = weight (kg) / (height (m) ** 2)

    Args:
        weight_kg: Body weight in kilograms.
        height_m: Height in meters.

    Returns:
        float: Calculated BMI value rounded to 2 decimal places.

    Raises:
        TypeError: If weight or height are not numeric types.
        ValueError: If weight or height are non-positive or exceed plausible limits.
    """
    if not isinstance(weight_kg, (int, float)) or not isinstance(height_m, (int, float)):
        raise TypeError("Weight and height must be numeric values.")

    if weight_kg <= 0:
        raise ValueError(f"Weight must be greater than zero. Received: {weight_kg}")

    if height_m <= 0:
        raise ValueError(f"Height must be greater than zero. Received: {height_m}")

    if weight_kg < MIN_WEIGHT_KG or weight_kg > MAX_WEIGHT_KG:
        raise ValueError(
            f"Weight ({weight_kg:.1f} kg) falls outside plausible physiological bounds "
            f"[{MIN_WEIGHT_KG} kg - {MAX_WEIGHT_KG} kg]."
        )

    if height_m < MIN_HEIGHT_M or height_m > MAX_HEIGHT_M:
        raise ValueError(
            f"Height ({height_m:.2f} m) falls outside plausible physiological bounds "
            f"[{MIN_HEIGHT_M} m - {MAX_HEIGHT_M} m]."
        )

    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def categorize_bmi(bmi: float) -> Tuple[str, str, str]:
    """
    Classifies a BMI value into standard World Health Organization (WHO) categories.

    Args:
        bmi: Body Mass Index value.

    Returns:
        Tuple of (Category Name, Health Advisory Message, Severity Color Code).

    Raises:
        TypeError: If BMI is not a numeric value.
        ValueError: If BMI is non-positive.
    """
    if not isinstance(bmi, (int, float)):
        raise TypeError("BMI must be a numeric value.")

    if bmi <= 0:
        raise ValueError("BMI value must be strictly positive.")

    if bmi < BMI_UNDERWEIGHT_MAX:
        category = "Underweight"
        advice = (
            "Your BMI suggests you may be underweight. It is recommended to consult a "
            "nutritionist or healthcare provider to ensure balanced nutrient intake."
        )
        color = "#1E88E5"  # Blue
    elif bmi < BMI_NORMAL_MAX:
        category = "Normal"
        advice = (
            "Congratulations! Your BMI is within the healthy weight range. "
            "Maintain your current balanced diet and regular physical activity."
        )
        color = "#2E7D32"  # Green
    elif bmi < BMI_OVERWEIGHT_MAX:
        category = "Overweight"
        advice = (
            "Your BMI indicates you are slightly above the optimal range. "
            "Adopting regular aerobic exercise and mindful portion control can be beneficial."
        )
        color = "#EF6C00"  # Orange
    else:
        category = "Obese"
        advice = (
            "Your BMI indicates obesity, which carries elevated risks of cardiovascular "
            "disease and metabolic conditions. Consulting a physician for guidance is advised."
        )
        color = "#C62828"  # Red

    return category, advice, color


def calculate_healthy_weight_range(height_m: float) -> Tuple[float, float]:
    """
    Calculates the recommended healthy weight range (kg) for a given height
    based on the standard normal BMI range (18.5 - 24.9).

    Args:
        height_m: Height in meters.

    Returns:
        Tuple of (minimum_healthy_kg, maximum_healthy_kg).
    """
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")

    min_weight = 18.5 * (height_m ** 2)
    max_weight = 24.9 * (height_m ** 2)
    return round(min_weight, 1), round(max_weight, 1)


# =====================================================================
# CLI (Command-Line Interface) Implementation
# =====================================================================

def display_cli_banner() -> None:
    """Displays a styled welcome banner for the CLI."""
    border = "=" * 66
    print("\n" + border)
    print("      OASIS INFOBYTE PYTHON INTERNSHIP - TASK 2")
    print("               BODY MASS INDEX (BMI) CALCULATOR")
    print(border)
    print("  Accurately assess your body mass index, WHO classification,")
    print("  and ideal healthy weight range with precision.")
    print(border + "\n")


def display_reference_chart() -> None:
    """Displays the WHO standard BMI reference chart."""
    print("\n" + "-" * 66)
    print("   WORLD HEALTH ORGANIZATION (WHO) BMI CLASSIFICATION CHART")
    print("-" * 66)
    print(f"   {'BMI Range (kg/m²)':<25} | {'Category':<15} | {'Health Risk':<18}")
    print("   " + "-" * 62)
    print(f"   {'Less than 18.5':<25} | {'Underweight':<15} | {'Nutritional deficit'}")
    print(f"   {'18.5 - 24.9':<25} | {'Normal':<15} | {'Low / Optimal'}")
    print(f"   {'25.0 - 29.9':<25} | {'Overweight':<15} | {'Moderate risk'}")
    print(f"   {'30.0 and above':<25} | {'Obese':<15} | {'High clinical risk'}")
    print("-" * 66 + "\n")


def prompt_positive_float(prompt_text: str, field_name: str, min_val: float, max_val: float) -> float:
    """
    Prompts the user repeatedly until a valid positive float within bounds is entered.
    Handles Ctrl+C and EOF gracefully.
    """
    while True:
        try:
            raw = input(prompt_text).strip()
            if not raw:
                print("   [!] Input cannot be empty. Please enter a numerical value.")
                continue

            value = float(raw)
            if value <= 0:
                print(f"   [!] Error: {field_name} must be strictly greater than zero.")
                continue

            if value < min_val or value > max_val:
                print(
                    f"   [!] Out of realistic range: {field_name} must be between "
                    f"{min_val} and {max_val}."
                )
                continue

            return value
        except ValueError:
            print(f"   [!] Invalid input: Please enter a valid number (e.g., 70 or 1.75).")
        except (KeyboardInterrupt, EOFError):
            print("\n\n   Operation canceled by user. Exiting session.")
            sys.exit(0)


def prompt_yes_no(prompt_text: str, default: bool = True) -> bool:
    """Prompts the user for a Yes/No answer with a default."""
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        try:
            choice = input(prompt_text + suffix).strip().lower()
            if not choice:
                return default
            if choice in ("y", "yes"):
                return True
            if choice in ("n", "no"):
                return False
            print("   [!] Please enter 'y' for Yes or 'n' for No.")
        except (KeyboardInterrupt, EOFError):
            print("\n   Operation canceled.")
            sys.exit(0)


def print_bmi_summary_card(weight_kg: float, height_m: float, bmi: float, category: str, advice: str) -> None:
    """Prints a structured summary card of the BMI assessment."""
    min_w, max_w = calculate_healthy_weight_range(height_m)
    border = "-" * 66

    print("\n" + border)
    print("                    BMI ASSESSMENT REPORT")
    print(border)
    print(f"   User Weight         : {weight_kg:.2f} kg")
    print(f"   User Height         : {height_m:.2f} m ({height_m * 100:.1f} cm)")
    print(f"   Calculated BMI      : {bmi:.2f} kg/m²")
    print(f"   Classification      : [{category.upper()}]")
    print(f"   Healthy Weight Span : {min_w:.1f} kg - {max_w:.1f} kg (for your height)")
    print(border)
    print("   Health Guidance:")
    print(f"   --> {advice}")
    print(border + "\n")


def run_cli_session() -> None:
    """Executes an interactive CLI calculation session."""
    print("Please enter your measurements below:")
    weight_kg = prompt_positive_float(
        prompt_text="   Enter your weight in kilograms (kg): ",
        field_name="Weight",
        min_val=MIN_WEIGHT_KG,
        max_val=MAX_WEIGHT_KG,
    )

    # Height input with smart unit handling option
    height_input = prompt_positive_float(
        prompt_text="   Enter your height (in meters e.g. 1.75, or cm e.g. 175): ",
        field_name="Height",
        min_val=MIN_HEIGHT_M,
        max_val=MAX_HEIGHT_M * 100,
    )

    # Auto-convert centimeters if user entered height > 3.0
    if height_input > MAX_HEIGHT_M:
        height_m = round(height_input / 100.0, 3)
        print(f"   [*] Detected height in centimeters: Converting {height_input:.1f} cm -> {height_m:.2f} m.")
    else:
        height_m = height_input

    bmi = calculate_bmi(weight_kg, height_m)
    category, advice, _ = categorize_bmi(bmi)
    print_bmi_summary_card(weight_kg, height_m, bmi, category, advice)


def run_cli_loop() -> None:
    """Interactive CLI menu loop."""
    display_cli_banner()
    while True:
        print("Main Menu:")
        print("  [1] Calculate BMI")
        print("  [2] View WHO Reference Chart")
        print("  [3] Launch Graphical GUI (Tkinter)")
        print("  [4] Exit Application")

        try:
            choice = input("\nSelect an option (1-4) [1]: ").strip()
            if not choice or choice == "1":
                run_cli_session()
            elif choice == "2":
                display_reference_chart()
            elif choice == "3":
                print("\nLaunching Graphical Interface...")
                launch_gui()
            elif choice == "4" or choice.lower() in ("q", "quit", "exit"):
                print("\nThank you for using the BMI Calculator. Stay healthy!\n")
                break
            else:
                print("   [!] Invalid option. Please select 1, 2, 3, or 4.")
                continue

            if choice == "1":
                if not prompt_yes_no("\nWould you like to perform another calculation?", default=True):
                    print("\nThank you for using the BMI Calculator. Stay healthy!\n")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Stay healthy!\n")
            break


# =====================================================================
# Tkinter GUI (Graphical User Interface) Implementation
# =====================================================================

def launch_gui() -> None:
    """
    Initializes and displays the modern Tkinter GUI application.
    Gracefully catches headless environments or missing display servers.
    """
    try:
        import tkinter as tk
        from tkinter import messagebox, ttk
    except ImportError as e:
        print(f"\n[ERROR] Tkinter is not available in this environment: {e}")
        return

    root = tk.Tk()
    root.title("Oasis Infobyte - BMI Calculator")
    root.geometry("540x680")
    root.minsize(480, 620)

    # Apply modern ttk theme
    style = ttk.Style(root)
    available_themes = style.theme_names()
    if "clam" in available_themes:
        style.theme_use("clam")

    # Colors and Fonts
    BG_COLOR = "#F4F6F9"
    HEADER_COLOR = "#1A237E"
    CARD_BG = "#FFFFFF"
    TEXT_MUTED = "#546E7A"

    root.configure(bg=BG_COLOR)

    # Header Frame
    header_frame = tk.Frame(root, bg=HEADER_COLOR, pady=18)
    header_frame.pack(fill=tk.X)

    title_label = tk.Label(
        header_frame,
        text="BODY MASS INDEX CALCULATOR",
        font=("Segoe UI", 15, "bold"),
        fg="#FFFFFF",
        bg=HEADER_COLOR,
    )
    title_label.pack()

    subtitle_label = tk.Label(
        header_frame,
        text="Oasis Infobyte Internship - Task 2",
        font=("Segoe UI", 9),
        fg="#C5CAE9",
        bg=HEADER_COLOR,
    )
    subtitle_label.pack(pady=(2, 0))

    # Main Content Container
    content_frame = tk.Frame(root, bg=BG_COLOR, padx=24, pady=16)
    content_frame.pack(fill=tk.BOTH, expand=True)

    # Input Card Frame
    input_card = tk.LabelFrame(
        content_frame,
        text="  Enter Your Measurements  ",
        font=("Segoe UI", 10, "bold"),
        bg=CARD_BG,
        fg="#263238",
        padx=18,
        pady=14,
        relief=tk.GROOVE,
    )
    input_card.pack(fill=tk.X, pady=(0, 14))

    # Unit selector for height
    height_unit_var = tk.StringVar(value="m")

    # Weight Input Row
    lbl_weight = tk.Label(
        input_card,
        text="Weight (kg):",
        font=("Segoe UI", 10),
        bg=CARD_BG,
        fg="#37474F",
    )
    lbl_weight.grid(row=0, column=0, sticky="w", pady=6)

    entry_weight = ttk.Entry(input_card, font=("Segoe UI", 10), width=18)
    entry_weight.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=6)
    entry_weight.focus()

    # Height Input Row
    lbl_height = tk.Label(
        input_card,
        text="Height:",
        font=("Segoe UI", 10),
        bg=CARD_BG,
        fg="#37474F",
    )
    lbl_height.grid(row=1, column=0, sticky="w", pady=6)

    entry_height = ttk.Entry(input_card, font=("Segoe UI", 10), width=18)
    entry_height.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=6)

    # Height Unit Toggle (meters or cm)
    unit_frame = tk.Frame(input_card, bg=CARD_BG)
    unit_frame.grid(row=1, column=2, padx=(10, 0), sticky="w")

    r_m = tk.Radiobutton(
        unit_frame,
        text="Meters (m)",
        variable=height_unit_var,
        value="m",
        bg=CARD_BG,
        font=("Segoe UI", 9),
    )
    r_m.pack(side=tk.LEFT)

    r_cm = tk.Radiobutton(
        unit_frame,
        text="Centimeters (cm)",
        variable=height_unit_var,
        value="cm",
        bg=CARD_BG,
        font=("Segoe UI", 9),
    )
    r_cm.pack(side=tk.LEFT, padx=(6, 0))

    # Results Card Frame
    result_card = tk.LabelFrame(
        content_frame,
        text="  BMI Assessment Results  ",
        font=("Segoe UI", 10, "bold"),
        bg=CARD_BG,
        fg="#263238",
        padx=18,
        pady=14,
        relief=tk.GROOVE,
    )
    result_card.pack(fill=tk.BOTH, expand=True, pady=(0, 14))

    # BMI Value Display
    lbl_bmi_title = tk.Label(
        result_card,
        text="Your Calculated BMI:",
        font=("Segoe UI", 9),
        fg=TEXT_MUTED,
        bg=CARD_BG,
    )
    lbl_bmi_title.pack(anchor="center")

    lbl_bmi_value = tk.Label(
        result_card,
        text="--.--",
        font=("Segoe UI", 28, "bold"),
        fg="#37474F",
        bg=CARD_BG,
    )
    lbl_bmi_value.pack(anchor="center")

    # Category Badge
    lbl_category_badge = tk.Label(
        result_card,
        text="Awaiting Input",
        font=("Segoe UI", 11, "bold"),
        fg="#FFFFFF",
        bg="#9E9E9E",
        padx=14,
        pady=4,
    )
    lbl_category_badge.pack(anchor="center", pady=(4, 10))

    # Ideal Weight Span
    lbl_healthy_range = tk.Label(
        result_card,
        text="Optimal weight range: --",
        font=("Segoe UI", 9, "italic"),
        fg=TEXT_MUTED,
        bg=CARD_BG,
    )
    lbl_healthy_range.pack(anchor="center", pady=(0, 8))

    # Health Advisory Note
    lbl_advisory = tk.Label(
        result_card,
        text="Enter weight and height above, then click 'Calculate BMI'.",
        font=("Segoe UI", 9),
        fg="#455A64",
        bg=CARD_BG,
        wraplength=420,
        justify=tk.CENTER,
    )
    lbl_advisory.pack(anchor="center", pady=(4, 0))

    # Action Logic
    def handle_calculate() -> None:
        raw_weight = entry_weight.get().strip()
        raw_height = entry_height.get().strip()

        if not raw_weight or not raw_height:
            messagebox.showwarning("Incomplete Input", "Please provide both weight and height.")
            return

        try:
            weight = float(raw_weight)
        except ValueError:
            messagebox.showerror("Invalid Input", "Weight must be a valid numeric value.")
            entry_weight.focus()
            return

        try:
            height = float(raw_height)
        except ValueError:
            messagebox.showerror("Invalid Input", "Height must be a valid numeric value.")
            entry_height.focus()
            return

        # Convert cm to meters if needed
        if height_unit_var.get() == "cm":
            height_m = height / 100.0
        else:
            # Automatic heuristic: If entered height > 3.0 in meters mode, likely entered cm
            if height > MAX_HEIGHT_M:
                height_m = height / 100.0
                height_unit_var.set("cm")
            else:
                height_m = height

        # Compute BMI with full domain validations
        try:
            bmi = calculate_bmi(weight, height_m)
            category, advice, color = categorize_bmi(bmi)
            min_w, max_w = calculate_healthy_weight_range(height_m)

            lbl_bmi_value.config(text=f"{bmi:.2f}", fg=color)
            lbl_category_badge.config(text=category.upper(), bg=color)
            lbl_healthy_range.config(
                text=f"Healthy Weight for your height: {min_w:.1f} kg – {max_w:.1f} kg"
            )
            lbl_advisory.config(text=advice)
        except ValueError as ex:
            messagebox.showerror("Validation Error", str(ex))

    def handle_reset() -> None:
        entry_weight.delete(0, tk.END)
        entry_height.delete(0, tk.END)
        height_unit_var.set("m")
        lbl_bmi_value.config(text="--.--", fg="#37474F")
        lbl_category_badge.config(text="Awaiting Input", bg="#9E9E9E")
        lbl_healthy_range.config(text="Optimal weight range: --")
        lbl_advisory.config(text="Enter weight and height above, then click 'Calculate BMI'.")
        entry_weight.focus()

    # Buttons Frame
    button_frame = tk.Frame(content_frame, bg=BG_COLOR)
    button_frame.pack(fill=tk.X, pady=(4, 0))

    btn_calc = tk.Button(
        button_frame,
        text="Calculate BMI",
        command=handle_calculate,
        font=("Segoe UI", 10, "bold"),
        bg="#1A237E",
        fg="#FFFFFF",
        activebackground="#283593",
        activeforeground="#FFFFFF",
        padx=18,
        pady=8,
        relief=tk.FLAT,
        cursor="hand2",
    )
    btn_calc.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 6))

    btn_reset = tk.Button(
        button_frame,
        text="Reset Fields",
        command=handle_reset,
        font=("Segoe UI", 10),
        bg="#ECEFF1",
        fg="#37474F",
        activebackground="#CFD8DC",
        activeforeground="#263238",
        padx=14,
        pady=8,
        relief=tk.FLAT,
        cursor="hand2",
    )
    btn_reset.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(6, 0))

    # Bind Enter key to calculation
    root.bind("<Return>", lambda event: handle_calculate())

    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()


# =====================================================================
# Main Application Entry Point
# =====================================================================

def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Oasis Infobyte Task 2: Advanced BMI Calculator (CLI & GUI)"
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Directly launch the Tkinter Graphical User Interface.",
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Directly launch the interactive Command-Line Interface.",
    )
    parser.add_argument(
        "-w",
        "--weight",
        type=float,
        help="Quick one-shot calculation: weight in kilograms.",
    )
    parser.add_argument(
        "-H",
        "--height",
        type=float,
        help="Quick one-shot calculation: height in meters.",
    )
    return parser.parse_args()


def main() -> None:
    """Primary entry point dispatching CLI or GUI."""
    args = parse_arguments()

    # One-shot CLI evaluation if both weight and height flags are supplied
    if args.weight is not None and args.height is not None:
        try:
            bmi = calculate_bmi(args.weight, args.height)
            category, advice, _ = categorize_bmi(bmi)
            print_bmi_summary_card(args.weight, args.height, bmi, category, advice)
            sys.exit(0)
        except (ValueError, TypeError) as err:
            print(f"[ERROR] {err}", file=sys.stderr)
            sys.exit(1)

    if args.gui:
        launch_gui()
    elif args.cli:
        run_cli_session()
    else:
        # Default user-friendly interactive menu
        run_cli_loop()


if __name__ == "__main__":
    main()

