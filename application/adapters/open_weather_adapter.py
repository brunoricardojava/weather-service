import httpx
import asyncio
from aiolimiter import AsyncLimiter

from django.conf import settings


class OpenWeatherAdpter:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(OpenWeatherAdpter, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, 'initialized'):
            self.base_url = settings.ENV_CONFIG.get("OPEN_WEATHER_BASE_URL")
            self.api_key = settings.ENV_CONFIG.get("API_KEY")
            self.units = "metric"
            self.client = httpx.AsyncClient()
            self.limiter = AsyncLimiter(max_rate=settings.ENV_CONFIG.get("MAX_RATE"), time_period=settings.ENV_CONFIG.get("TIME_PERIOD"))
            self.initialized = True

    async def execute(self, city_id) -> dict:
        return await self.fetch_weather(city_id)

    async def fetch_weather(self,city_id) -> dict:
        params = {
            "id": city_id,
            "appid": self.api_key,
            "units": self.units
        }
        async with self.limiter:
            while True:
                try:
                    response = await self.client.get(url=self.base_url, params=params)
                except:
                    print("Sleeping for 5 seconds")
                    await asyncio.sleep(5)
                else:
                    return response
