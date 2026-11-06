"""
Unit tests for the Random Password Generator module.
Ensures validation, character constraints, and CSPRNG behavior work properly.
"""

import string
import unittest

from main import (
    MIN_PASSWORD_LENGTH,
    evaluate_strength,
    generate_password,
)


class TestPasswordGenerator(unittest.TestCase):
    def test_default_generation(self):
        """Test default password generation with 16 characters."""
        length = 16
        password = generate_password(length)
        self.assertEqual(len(password), length)

        # Check all sets are represented
        self.assertTrue(any(c in string.ascii_uppercase for c in password))
        self.assertTrue(any(c in string.ascii_lowercase for c in password))
        self.assertTrue(any(c in string.digits for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))

    def test_minimum_length_enforced(self):
        """Test that lengths below MIN_PASSWORD_LENGTH raise ValueError."""
        with self.assertRaises(ValueError):
            generate_password(MIN_PASSWORD_LENGTH - 1)

    def test_no_character_set_selected(self):
        """Test that selecting zero sets raises ValueError."""
        with self.assertRaises(ValueError):
            generate_password(
                length=10,
                use_upper=False,
                use_lower=False,
                use_digits=False,
                use_symbols=False,
            )

    def test_single_character_set_digits_only(self):
        """Test generating digits-only PIN/password."""
        password = generate_password(
            length=10,
            use_upper=False,
            use_lower=False,
            use_digits=True,
            use_symbols=False,
        )
        self.assertEqual(len(password), 10)
        self.assertTrue(password.isdigit())

    def test_alphanumeric_no_symbols(self):
        """Test generating password without symbols."""
        password = generate_password(
            length=20,
            use_upper=True,
            use_lower=True,
            use_digits=True,
            use_symbols=False,
        )
        self.assertEqual(len(password), 20)
        self.assertFalse(any(c in string.punctuation for c in password))
        self.assertTrue(any(c in string.ascii_uppercase for c in password))
        self.assertTrue(any(c in string.ascii_lowercase for c in password))
        self.assertTrue(any(c in string.digits for c in password))

    def test_uniqueness_and_randomness(self):
        """Test that successive passwords are not identical."""
        passwords = {generate_password(16) for _ in range(50)}
        self.assertEqual(len(passwords), 50, "All 50 generated passwords should be unique.")

    def test_strength_evaluator(self):
        """Test password strength rating logic."""
        level, _ = evaluate_strength(length=20, num_categories=4)
        self.assertEqual(level, "Very Strong")

        level, _ = evaluate_strength(length=14, num_categories=3)
        self.assertEqual(level, "Strong")

        level, _ = evaluate_strength(length=10, num_categories=2)
        self.assertEqual(level, "Moderate")

        level, _ = evaluate_strength(length=8, num_categories=1)
        self.assertEqual(level, "Weak")


if __name__ == "__main__":
    unittest.main()

