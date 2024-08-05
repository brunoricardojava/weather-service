import pytest
from httpx import AsyncClient
from django.test import override_settings
from unittest.mock import patch, AsyncMock, MagicMock

from application.adapters import OpenWeatherAdpter


class TestOpenWeatherAdapter:
    """Test OpenWeatherAdapter"""

    @pytest.mark.asyncio
    @override_settings(ENV_CONFIG={"OPEN_WEATHER_BASE_URL": "http://mock-api-url","API_KEY": "mock-api-key","MAX_RATE": 50,"TIME_PERIOD": 60})
    async def test_singleton_instance(self):
        adapter1 = OpenWeatherAdpter()
        adapter2 = OpenWeatherAdpter()
        assert adapter1 is adapter2

    @pytest.mark.asyncio
    @patch.object(AsyncClient, "get")
    @override_settings(ENV_CONFIG={"OPEN_WEATHER_BASE_URL": "http://mock-api-url","API_KEY": "mock-api-key","MAX_RATE": 50,"TIME_PERIOD": 60})
    async def test_fetch_weather_success(self, mock_async_client):
        mock_async_client.return_value = MagicMock(status_code=200, json=lambda: {"weather": "data"})

        adapter = OpenWeatherAdpter()
        response = await adapter.execute(city_id=123)

        assert response.status_code == 200
        assert response.json() == {"weather": "data"}

    @pytest.mark.asyncio
    @patch.object(AsyncClient, "get")
    @patch.dict('django.conf.settings.ENV_CONFIG', {
        "OPEN_WEATHER_BASE_URL": "http://mock-api-url",
        "API_KEY": "mock-api-key",
        "MAX_RATE": 50,
        "TIME_PERIOD": 60
    })
    async def test_fetch_weather_retry_on_failure(self, mock_async_client):
        mock_async_client.side_effect = [Exception("Connection error"), MagicMock(status_code=500, json=lambda: {})]

        adapter = OpenWeatherAdpter()
        response = await adapter.execute(city_id=123)
        
        assert response.status_code == 500
        assert response.json() == {}
