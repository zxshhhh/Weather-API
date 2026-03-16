from rest_framework import serializers

class CountrySerializer(serializers.Serializer):
    name = serializers.CharField()
    capital = serializers.ListField(child=serializers.CharField(), required=False)
    region = serializers.CharField()
    population = serializers.IntegerField()
    flags = serializers.DictField()

class WeatherSerializer(serializers.Serializer):
    temperature = serializers.FloatField(source='main.temp')
    description = serializers.SerializerMethodField()
    humidity = serializers.IntegerField(source='main.humidity')
    wind_speed = serializers.FloatField(source='wind.speed')

    def get_description(self, obj):
        """Safely extract description from weather[0]"""
        weather_list = obj.get('weather')
        if isinstance(weather_list, list) and len(weather_list) > 0:
            return weather_list[0].get('description')
        return None

class CountryWeatherSerializer(serializers.Serializer):
    country = CountrySerializer()
    weather = WeatherSerializer()