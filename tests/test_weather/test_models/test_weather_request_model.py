import pytest
from datetime import datetime
from django.utils import timezone


@pytest.mark.django_db
class TestWeatherRequestModel:
    """Test WeatherRequestModel"""

    NOW = timezone.now()

    def test_representer_model(self, fixture_weather_request_model):
        weather_request_model = fixture_weather_request_model

        assert isinstance(weather_request_model.created_at, datetime)
        assert weather_request_model.created_at > self.NOW
        assert str(weather_request_model) == str(weather_request_model.request_id)
