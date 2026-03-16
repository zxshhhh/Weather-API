from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
import logging

from .services import CountryClient
from .services import WeatherClient
from .serializers import CountryWeatherSerializer

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """Global error handler"""
    response = Response(
        {"error": str(exc), "detail": "External API failed"},
        status=status.HTTP_503_SERVICE_UNAVAILABLE
    )
    return response

class CountryWeatherView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(name='country', description='Country name (e.g. philippines)', required=True, type=str)
        ],
        responses={200: CountryWeatherSerializer}
    )
    def get(self, request, version):
        country_name = request.query_params.get('country')
        if not country_name:
            return Response({"error": "country query param required"}, status=400)

        try:
            countries = CountryClient.get_by_name(country_name)
            if not countries:
                return Response({"error": "Country not found"}, status=404)
            
            country = countries[0]
            capital = country.get('capital', [None])[0]
            
            if not capital:
                return Response({"error": "No capital found"}, status=404)
            
            weather_data = WeatherClient.get_by_city(capital)
            
            combined_data = {
                "country": {
                    "name": country['name']['common'],
                    "capital": country.get('capital', []),
                    "region": country.get('region', ''),
                    "population": country.get('population', 0),
                    "flags": country.get('flags', {}),
                },
                "weather": weather_data,
            }
            
            serializer = CountryWeatherSerializer(combined_data)
            return Response(serializer.data, status=200)

        except Exception as e:
            logger.exception("Integration failed")
            return Response({"error": "Service unavailable"}, status=503)