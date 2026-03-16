from django.urls import path
from .views import CountryWeatherView

urlpatterns = [
    path('country-weather/', CountryWeatherView.as_view(), name='country-weather'),
]