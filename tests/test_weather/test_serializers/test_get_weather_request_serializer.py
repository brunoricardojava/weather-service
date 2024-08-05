import pytest
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import ValidationError

from weather.serializers import GetWeatherRequestSerializer


@pytest.mark.django_db
class TestGetWeatherRequestSerializer:
    """Test GetWeatherRequestSerializer"""

    serializer_to_test = GetWeatherRequestSerializer

    def test_valid_weather_request_data(self, fixture_valid_weather_request_data):
        serializer = self.serializer_to_test(data=fixture_valid_weather_request_data)

        assert serializer.is_valid()
        assert serializer.validated_data == fixture_valid_weather_request_data

    def test_invalid_weather_request_data(self, fixture_valid_weather_request_data):
        fixture_valid_weather_request_data["request_id"] = 10
        serializer = self.serializer_to_test(data=fixture_valid_weather_request_data)

        expected_erros = {'request_id': [ErrorDetail(string='WeatherRequest with id: 10 does not exist.', code='invalid')]}

        assert not serializer.is_valid()
        assert serializer.errors == expected_erros
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
