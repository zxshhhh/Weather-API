from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient

class CountryWeatherTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('weather.services.CountryClient.get_by_name')
    @patch('weather.services.WeatherClient.get_by_city')
    def test_combined_endpoint(self, mock_weather, mock_country):
        mock_country.return_value = [{
            "name": {"common": "Philippines"},
            "capital": ["Manila"],
            "region": "Asia",
            "population": 11300000,
            "flags": {"png": "https://flagcdn.com/ph.png"}
        }]
        mock_weather.return_value = {
            "main": {"temp": 28.5, "humidity": 75},
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 3.2}
        }

        response = self.client.get('/api/v1/country-weather/?country=philippines')
        self.assertEqual(response.status_code, 200)
        self.assertIn('country', response.data)
        self.assertIn('weather', response.data)