"""
Oasis Infobyte Internship - Python Development
Task 3: Random Password Generator
Author: Silambarasan (OIBSIP Intern)
Description: A cryptographically secure, customizable random password generator
             command-line application built with Python.
"""

import secrets
import string
import sys
from typing import Dict, List, Tuple


# Configuration Constants
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128


def get_character_sets() -> Dict[str, Tuple[str, str]]:
    """
    Returns available character sets with their descriptions and character pools.
    """
    return {
        "uppercase": ("Uppercase letters (A-Z)", string.ascii_uppercase),
        "lowercase": ("Lowercase letters (a-z)", string.ascii_lowercase),
        "digits": ("Numbers (0-9)", string.digits),
        "symbols": ("Special symbols (!@#$%^&* etc.)", string.punctuation),
    }


def evaluate_strength(length: int, num_categories: int) -> Tuple[str, str]:
    """
    Evaluates password strength based on length and variety of character types.

    Returns:
        Tuple of (strength_label, description)
    """
    if length >= 16 and num_categories == 4:
        return "Very Strong", "Excellent entropy. Resistant to brute-force and dictionary attacks."
    elif length >= 12 and num_categories >= 3:
        return "Strong", "Good security for most sensitive accounts and services."
    elif length >= 8 and num_categories >= 2:
        return "Moderate", "Meets minimum baseline criteria, but could be longer or more diverse."
    else:
        return "Weak", "Vulnerable to automated cracking. Consider increasing length and variety."


def generate_password(
    length: int,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """
    Generates a cryptographically secure password with the specified length and character types.

    Guarantees at least one character from each selected category to ensure compliance
    with strict password policies.

    Args:
        length: Desired length of the password (>= 8).
        use_upper: Include uppercase letters.
        use_lower: Include lowercase letters.
        use_digits: Include numeric digits.
        use_symbols: Include punctuation / special characters.

    Returns:
        A securely generated random password string.

    Raises:
        ValueError: If length is less than MIN_PASSWORD_LENGTH or no character set is selected.
    """
    if length < MIN_PASSWORD_LENGTH:
        raise ValueError(
            f"Password length must be at least {MIN_PASSWORD_LENGTH} characters."
        )

    char_pool_map = {
        "upper": (use_upper, string.ascii_uppercase),
        "lower": (use_lower, string.ascii_lowercase),
        "digits": (use_digits, string.digits),
        "symbols": (use_symbols, string.punctuation),
    }

    selected_pools: List[str] = [
        chars for enabled, chars in char_pool_map.values() if enabled
    ]

    if not selected_pools:
        raise ValueError("At least one character type must be selected.")

    # Guarantee at least one character from each selected category
    password_chars: List[str] = [
        secrets.choice(pool) for pool in selected_pools
    ]

    # Combine all selected pools for remaining characters
    combined_pool = "".join(selected_pools)
    remaining_length = length - len(password_chars)

    for _ in range(remaining_length):
        password_chars.append(secrets.choice(combined_pool))

    # Securely shuffle characters using SystemRandom (CSPRNG)
    # This prevents the guaranteed characters from appearing in a predictable order
    cryptogen = secrets.SystemRandom()
    cryptogen.shuffle(password_chars)

    return "".join(password_chars)


def prompt_yes_no(question: str, default: bool = True) -> bool:
    """
    Prompts the user for a yes/no response with a specified default.
    """
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        try:
            choice = input(question + suffix).strip().lower()
            if not choice:
                return default
            if choice in ("y", "yes"):
                return True
            if choice in ("n", "no"):
                return False
            print("  [!] Please enter 'y' for Yes or 'n' for No.")
        except (KeyboardInterrupt, EOFError):
            print("\n  Operation canceled.")
            sys.exit(0)


def prompt_password_length() -> int:
    """
    Prompts the user for password length and enforces minimum/maximum limits.
    """
    while True:
        try:
            raw_input = input(
                f"\nEnter desired password length (min {MIN_PASSWORD_LENGTH}, max {MAX_PASSWORD_LENGTH}) [default 16]: "
            ).strip()

            if not raw_input:
                return 16

            length = int(raw_input)
            if length < MIN_PASSWORD_LENGTH:
                print(
                    f"  [!] Invalid length: Password must be at least {MIN_PASSWORD_LENGTH} characters."
                )
                continue
            if length > MAX_PASSWORD_LENGTH:
                print(
                    f"  [!] Invalid length: Maximum supported length is {MAX_PASSWORD_LENGTH}."
                )
                continue

            return length
        except ValueError:
            print("  [!] Invalid input: Please enter a valid positive integer.")
        except (KeyboardInterrupt, EOFError):
            print("\n  Operation canceled.")
            sys.exit(0)


def display_header() -> None:
    """Prints a styled welcome header."""
    print("=" * 64)
    print("   OASIS INFOBYTE PYTHON INTERNSHIP - TASK 3")
    print("        CRYPTOGRAPHIC RANDOM PASSWORD GENERATOR")
    print("=" * 64)
    print("  Generate strong, unpredictable, and customizable passwords")
    print("  powered by Python's 'secrets' module (CSPRNG).\n")


def print_password_card(password: str, strength: str, description: str) -> None:
    """Displays the generated password in a clean visual card."""
    border = "-" * 64
    print("\n" + border)
    print("  GENERATED PASSWORD:")
    print(f"  --> {password}")
    print(border)
    print(f"  Length        : {len(password)} characters")
    print(f"  Strength Level: {strength}")
    print(f"  Assessment    : {description}")
    print(border + "\n")


def run_generator_session() -> None:
    """Runs a single password generation session."""
    length = prompt_password_length()

    print("\nSelect character types to include:")
    while True:
        include_upper = prompt_yes_no("  Include Uppercase letters (A-Z)?", default=True)
        include_lower = prompt_yes_no("  Include Lowercase letters (a-z)?", default=True)
        include_digits = prompt_yes_no("  Include Numbers (0-9)?", default=True)
        include_symbols = prompt_yes_no("  Include Special symbols (!@#$%...)?", default=True)

        selected_count = sum([include_upper, include_lower, include_digits, include_symbols])

        if selected_count == 0:
            print("\n  [ERROR] You must select at least one character type!\n  Please try again.\n")
            continue
        break

    try:
        password = generate_password(
            length=length,
            use_upper=include_upper,
            use_lower=include_lower,
            use_digits=include_digits,
            use_symbols=include_symbols,
        )
        strength, desc = evaluate_strength(length, selected_count)
        print_password_card(password, strength, desc)
    except ValueError as err:
        print(f"\n  [ERROR] Generation failed: {err}")


def main() -> None:
    """Main application loop."""
    display_header()

    while True:
        run_generator_session()
        again = prompt_yes_no("Would you like to generate another password?", default=True)
        if not again:
            print("\nThank you for using the Random Password Generator. Goodbye!\n")
            break


if __name__ == "__main__":
    main()

