import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from application.use_cases import CollectWeatherUseCase
from weather.serializers import WeatherRequestSerializer
from weather.models import WeatherInfo


@pytest.mark.django_db
class TestWeatherView:
    """Test WeatherView"""

    api_client = APIClient()

    @patch.object(CollectWeatherUseCase, "execute")
    def test_post_valid_data_weather_view(self, mock_usecase_execute):
        mock_usecase_execute.return_value = None
        url = reverse(viewname="WeatherRoute", kwargs={"request_id": 1})
        response = self.api_client.post(path=url, format="json")

        expected_response = {"Response": "All OK. S2"}

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_response

    def test_post_invalid_data_weather_view(self, fixture_weather_request_model):
        weather_request = fixture_weather_request_model
        url = reverse(viewname="WeatherRoute", kwargs={"request_id": weather_request.request_id})
        response = self.api_client.post(path=url, format="json")

        expected_error = {'request_id': [ErrorDetail(string='weather request with this request id already exists.', code='unique')]}

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == expected_error

    @patch.object(WeatherRequestSerializer, "save")
    def test_internal_error_post_weather_view(self, mock_serializer_save):
        mock_serializer_save.side_effect = Exception("Erro serializer save")
        url = reverse(viewname="WeatherRoute", kwargs={"request_id": 1})
        response = self.api_client.post(path=url, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data == {}

    @patch.object(WeatherInfo.objects, "filter")
    def test_get_valid_data_weather_view(self, mock_model_filter, fixture_weather_request_model):
        mock_count = MagicMock()
        mock_count.count.return_value = 5
        mock_model_filter.return_value = mock_count
        weather_request_model = fixture_weather_request_model
        url = reverse(viewname="WeatherRoute", kwargs={"request_id": 1})
        response = self.api_client.get(path=url, format="json")

        expected_response = {"Total Percent": int((5 * 100)/167)}

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_response

    @patch.object(WeatherInfo.objects, "filter")
    def test_get_invalid_data_weather_view(self, mock_model_filter, fixture_weather_request_model):
        mock_count = MagicMock()
        mock_count.count.return_value = 5
        mock_model_filter.return_value = mock_count
        weather_request_model = fixture_weather_request_model
        url = reverse(viewname="WeatherRoute", kwargs={"request_id": 10})
        response = self.api_client.get(path=url, format="json")

        expected_error = {'request_id': [ErrorDetail(string='WeatherRequest with id: 10 does not exist.', code='invalid')]}

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == expected_error

    @patch.object(WeatherInfo.objects, "filter")
    def test_internal_error_get_weather_view(self, mock_model_filter, fixture_weather_request_model):
        mock_model_filter.side_effect = Exception("Erro model filter")
        weather_request_model = fixture_weather_request_model
        url = reverse(viewname="WeatherRoute", kwargs={"request_id": weather_request_model.request_id})
        response = self.api_client.get(path=url, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data == {}
