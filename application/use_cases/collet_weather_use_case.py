import asyncio
import json
from asgiref.sync import sync_to_async

from rest_framework.response import Response

from weather.utils.city_id_list import CITY_ID_LIST
from weather.models import WeatherInfo, WeatherRequest

from application.adapters import OpenWeatherAdpter


class ColletWeatherUseCase:

    def __init__(self, weather_request: WeatherRequest, weather_consumer = OpenWeatherAdpter()) -> None:
        self.weather_request = weather_request
        self.weather_consumer = weather_consumer

    def execute(self):
        asyncio.run(self._process())

    async def _process(self):
        responses = await self._fetch_data()
        await self._process_responses(responses)

    async def _fetch_data(self):
        tasks = []
        for city_id in CITY_ID_LIST[:5]:
            tasks.append(self.weather_consumer.execute(city_id))
        responses = await asyncio.gather(*tasks)
        return responses

    async def _process_responses(self, responses: list[Response]):
        for response in responses:
            data = response.json()
            data_to_storage = {
                "city_id": data.get("id"),
                "temperature": data.get("main").get("temp"),
                "humidity": data.get("main").get("humidity")
            }
            await sync_to_async(WeatherInfo.objects.create)(
                weather_request=self.weather_request,
                city_id=data.get("id"),
                weather_data=json.dumps(data_to_storage),
            )
