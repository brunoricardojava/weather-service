import httpx
from aiolimiter import AsyncLimiter

class OpenWeatherAdpter:
    def __init__(self) -> None:
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.api_key = "0ebd639c1938fcc6c839718735b6dc86"
        self.units = "metric"
        self.client = httpx.AsyncClient()
        self.limiter = AsyncLimiter(max_rate=60, time_period=1)

    async def execute(self, city_id) -> dict:
        return await self.fetch_weather(city_id)

    async def fetch_weather(self,city_id) -> dict:
        params = {
            "id": city_id,
            "appid": self.api_key,
            "units": self.units
        }
        async with self.limiter:
            response = await self.client.get(url=self.base_url, params=params)
            return response
