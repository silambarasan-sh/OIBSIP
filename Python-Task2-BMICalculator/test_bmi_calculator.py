"""
Unit tests for the BMI Calculator module.
Validates mathematical calculations, WHO category boundaries,
physiological range constraints, and robust input validation.
"""

import unittest

from main import (
    BMI_NORMAL_MAX,
    BMI_OVERWEIGHT_MAX,
    BMI_UNDERWEIGHT_MAX,
    calculate_bmi,
    calculate_healthy_weight_range,
    categorize_bmi,
)


class TestBMICalculation(unittest.TestCase):
    """Tests the mathematical accuracy and precision of the BMI calculation."""

    def test_standard_normal_bmi(self):
        """Test standard normal case: 70kg, 1.75m -> 22.86."""
        bmi = calculate_bmi(70.0, 1.75)
        expected = round(70.0 / (1.75 ** 2), 2)
        self.assertEqual(bmi, expected)
        self.assertEqual(bmi, 22.86)

    def test_underweight_calculation(self):
        """Test calculation resulting in underweight value."""
        bmi = calculate_bmi(45.0, 1.75)
        self.assertEqual(bmi, 14.69)

    def test_overweight_calculation(self):
        """Test calculation resulting in overweight value."""
        bmi = calculate_bmi(85.0, 1.75)
        self.assertEqual(bmi, 27.76)

    def test_obese_calculation(self):
        """Test calculation resulting in obese value."""
        bmi = calculate_bmi(110.0, 1.75)
        self.assertEqual(bmi, 35.92)

    def test_integer_inputs_accepted(self):
        """Test that int arguments are accepted and converted properly."""
        bmi = calculate_bmi(80, 2)
        self.assertEqual(bmi, 20.0)


class TestBMICategorization(unittest.TestCase):
    """Tests World Health Organization (WHO) threshold classifications and boundary transitions."""

    def test_underweight_classification(self):
        category, _, color = categorize_bmi(16.0)
        self.assertEqual(category, "Underweight")
        self.assertEqual(color, "#1E88E5")

    def test_boundary_just_below_normal(self):
        category, _, _ = categorize_bmi(18.49)
        self.assertEqual(category, "Underweight")

    def test_boundary_exact_normal_lower(self):
        category, _, color = categorize_bmi(18.5)
        self.assertEqual(category, "Normal")
        self.assertEqual(color, "#2E7D32")

    def test_normal_classification(self):
        category, _, _ = categorize_bmi(22.0)
        self.assertEqual(category, "Normal")

    def test_boundary_just_below_overweight(self):
        category, _, _ = categorize_bmi(24.99)
        self.assertEqual(category, "Normal")

    def test_boundary_exact_overweight_lower(self):
        category, _, color = categorize_bmi(25.0)
        self.assertEqual(category, "Overweight")
        self.assertEqual(color, "#EF6C00")

    def test_overweight_classification(self):
        category, _, _ = categorize_bmi(27.5)
        self.assertEqual(category, "Overweight")

    def test_boundary_just_below_obese(self):
        category, _, _ = categorize_bmi(29.99)
        self.assertEqual(category, "Overweight")

    def test_boundary_exact_obese_lower(self):
        category, _, color = categorize_bmi(30.0)
        self.assertEqual(category, "Obese")
        self.assertEqual(color, "#C62828")

    def test_severe_obesity_classification(self):
        category, _, _ = categorize_bmi(45.0)
        self.assertEqual(category, "Obese")


class TestInputValidationAndErrors(unittest.TestCase):
    """Tests error handling for invalid data types, zero/negative values, and out-of-range bounds."""

    def test_zero_height_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            calculate_bmi(70.0, 0.0)
        self.assertIn("greater than zero", str(ctx.exception).lower())

    def test_negative_height_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            calculate_bmi(70.0, -1.75)
        self.assertIn("greater than zero", str(ctx.exception).lower())

    def test_zero_weight_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            calculate_bmi(0.0, 1.75)
        self.assertIn("greater than zero", str(ctx.exception).lower())

    def test_negative_weight_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            calculate_bmi(-65.0, 1.75)
        self.assertIn("greater than zero", str(ctx.exception).lower())

    def test_non_numeric_weight_raises_type_error(self):
        with self.assertRaises(TypeError):
            calculate_bmi("seventy", 1.75)  # type: ignore

    def test_non_numeric_height_raises_type_error(self):
        with self.assertRaises(TypeError):
            calculate_bmi(70.0, None)  # type: ignore

    def test_unrealistically_low_weight(self):
        with self.assertRaises(ValueError) as ctx:
            calculate_bmi(0.5, 1.75)
        self.assertIn("outside plausible physiological bounds", str(ctx.exception))

    def test_unrealistically_high_weight(self):
        with self.assertRaises(ValueError) as ctx:
            calculate_bmi(700.0, 1.75)
        self.assertIn("outside plausible physiological bounds", str(ctx.exception))

    def test_unrealistically_low_height(self):
        with self.assertRaises(ValueError) as ctx:
            calculate_bmi(60.0, 0.20)
        self.assertIn("outside plausible physiological bounds", str(ctx.exception))

    def test_unrealistically_high_height(self):
        with self.assertRaises(ValueError) as ctx:
            calculate_bmi(70.0, 3.50)
        self.assertIn("outside plausible physiological bounds", str(ctx.exception))

    def test_categorize_non_numeric_raises_type_error(self):
        with self.assertRaises(TypeError):
            categorize_bmi("invalid")  # type: ignore

    def test_categorize_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            categorize_bmi(-5.0)


class TestHealthyWeightRange(unittest.TestCase):
    """Tests healthy weight range estimation."""

    def test_healthy_weight_range_calculation(self):
        min_w, max_w = calculate_healthy_weight_range(1.75)
        self.assertEqual(min_w, 56.7)
        self.assertEqual(max_w, 76.3)

    def test_healthy_range_invalid_height(self):
        with self.assertRaises(ValueError):
            calculate_healthy_weight_range(0.0)


if __name__ == "__main__":
    unittest.main()

