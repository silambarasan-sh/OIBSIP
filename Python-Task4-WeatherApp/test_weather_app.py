"""
Unit tests for the Weather App module.
Validates metric conversions, JSON response parsing, error handling,
offline demo functionality, and simulated HTTP responses.
"""

import unittest
from unittest.mock import MagicMock, patch

from main import (
    convert_celsius_to_fahrenheit,
    convert_mps_to_kmh,
    convert_mps_to_mph,
    fetch_weather,
    get_mock_weather,
    parse_weather_payload,
)


class TestUnitConversions(unittest.TestCase):
    """Tests accuracy of temperature and velocity mathematical conversions."""

    def test_celsius_to_fahrenheit_freezing(self):
        self.assertEqual(convert_celsius_to_fahrenheit(0.0), 32.0)

    def test_celsius_to_fahrenheit_boiling(self):
        self.assertEqual(convert_celsius_to_fahrenheit(100.0), 212.0)

    def test_celsius_to_fahrenheit_room_temp(self):
        self.assertEqual(convert_celsius_to_fahrenheit(25.0), 77.0)

    def test_celsius_to_fahrenheit_negative_equality(self):
        self.assertEqual(convert_celsius_to_fahrenheit(-40.0), -40.0)

    def test_mps_to_kmh(self):
        self.assertEqual(convert_mps_to_kmh(10.0), 36.0)
        self.assertEqual(convert_mps_to_kmh(0.0), 0.0)

    def test_mps_to_mph(self):
        self.assertEqual(convert_mps_to_mph(10.0), 22.37)
        self.assertEqual(convert_mps_to_mph(0.0), 0.0)


class TestPayloadParsing(unittest.TestCase):
    """Tests JSON payload extraction and object transformation."""

    def setUp(self):
        self.sample_payload = {
            "name": "Coimbatore",
            "sys": {"country": "IN"},
            "main": {
                "temp": 28.5,
                "feels_like": 31.0,
                "humidity": 65,
                "pressure": 1012,
            },
            "weather": [
                {"main": "Clouds", "description": "few clouds"}
            ],
            "wind": {"speed": 4.5},
            "visibility": 8000,
        }

    def test_parse_valid_payload(self):
        report = parse_weather_payload(self.sample_payload)
        self.assertEqual(report.city_name, "Coimbatore")
        self.assertEqual(report.country, "IN")
        self.assertEqual(report.temp_c, 28.5)
        self.assertEqual(report.temp_f, 83.3)
        self.assertEqual(report.feels_like_c, 31.0)
        self.assertEqual(report.humidity, 65)
        self.assertEqual(report.pressure_hpa, 1012)
        self.assertEqual(report.condition, "Clouds")
        self.assertEqual(report.description, "Few clouds")
        self.assertEqual(report.wind_speed_mps, 4.5)
        self.assertEqual(report.wind_speed_kmh, 16.2)
        self.assertEqual(report.visibility_km, 8.0)
        self.assertFalse(report.is_demo)

    def test_missing_mandatory_keys_raises_value_error(self):
        invalid_payload = {"name": "Chennai"}  # Missing 'main'
        with self.assertRaises(ValueError):
            parse_weather_payload(invalid_payload)

    def test_non_dict_payload_raises_value_error(self):
        with self.assertRaises(ValueError):
            parse_weather_payload("not a dictionary")  # type: ignore


class TestMockAndFallback(unittest.TestCase):
    """Tests the offline fallback mechanism for smooth demonstrations."""

    def test_known_mock_city_chennai(self):
        report = get_mock_weather("Chennai")
        self.assertEqual(report.city_name, "Chennai")
        self.assertEqual(report.country, "IN")
        self.assertTrue(report.is_demo)

    def test_known_mock_city_london(self):
        report = get_mock_weather("London")
        self.assertEqual(report.city_name, "London")
        self.assertEqual(report.country, "GB")
        self.assertTrue(report.is_demo)

    def test_generic_mock_fallback_for_unknown_city(self):
        report = get_mock_weather("SampleTown")
        self.assertEqual(report.city_name, "Sampletown")
        self.assertTrue(report.is_demo)
        self.assertEqual(report.temp_c, 25.0)


class TestInputValidation(unittest.TestCase):
    """Tests validation for empty inputs."""

    def test_empty_query_raises_value_error(self):
        with self.assertRaises(ValueError):
            fetch_weather("")

    def test_whitespace_query_raises_value_error(self):
        with self.assertRaises(ValueError):
            fetch_weather("   ")


class TestNetworkAndErrorHandling(unittest.TestCase):
    """Simulates network scenarios and HTTP response codes."""

    @patch("main.requests.get")
    def test_simulated_http_200_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Madurai",
            "sys": {"country": "IN"},
            "main": {"temp": 33.0, "feels_like": 37.0, "humidity": 70, "pressure": 1010},
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "wind": {"speed": 2.5},
            "visibility": 10000,
        }
        mock_get.return_value = mock_response

        report = fetch_weather(query="Madurai", api_key="test_valid_key", use_demo=False)
        self.assertEqual(report.city_name, "Madurai")
        self.assertEqual(report.temp_c, 33.0)
        self.assertFalse(report.is_demo)

    @patch("main.requests.get")
    def test_simulated_http_404_city_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "city not found"}
        mock_get.return_value = mock_response

        with self.assertRaises(LookupError) as ctx:
            fetch_weather(query="NonExistentCityXYZ", api_key="test_key", use_demo=False)
        self.assertIn("not found", str(ctx.exception).lower())

    @patch("main.requests.get")
    def test_simulated_http_401_invalid_key(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "Invalid API key"}
        mock_get.return_value = mock_response

        with self.assertRaises(PermissionError):
            fetch_weather(query="London", api_key="invalid_or_inactive_key", use_demo=False)


if __name__ == "__main__":
    unittest.main()
