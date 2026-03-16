import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class CountryClient:
    BASE_URL = "https://restcountries.com/v3.1"
    @staticmethod
    def get_by_name(name: str):
        try:
            response = requests.get(f"{CountryClient.BASE_URL}/name/{name}", timeout=10)
            if response.status_code == 404:
                return []
            response.raise_for_status()
            return response.json()  # list of countries
        except requests.exceptions.RequestException as e:
            logger.error(f"Country API error: {e}")
            raise

class WeatherClient:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    @staticmethod
    def get_by_city(city: str, units="metric"):
        try:
            params = {
                "q": city,
                "appid": settings.OPENWEATHERMAP_API_KEY,
                "units": units,
            }
            response = requests.get(WeatherClient.BASE_URL, params=params, timeout=10)
            if response.status_code == 404:
                return []
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API error: {e}")
            raise