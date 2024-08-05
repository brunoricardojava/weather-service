from pytest import fixture
from django.conf import settings
from unittest.mock import MagicMock
 
from weather.models import WeatherRequest

@fixture
def fixture_weather_request_model() -> WeatherRequest:
    return WeatherRequest.objects.create(request_id=1)

@fixture
def fixture_valid_weather_request_data(fixture_weather_request_model) -> dict:
    return {
        "request_id": fixture_weather_request_model.request_id
    }

@fixture
def weather_request():
    return MagicMock(spec=WeatherRequest)
