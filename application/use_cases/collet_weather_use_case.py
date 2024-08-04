import asyncio
import json
from asgiref.sync import sync_to_async

from rest_framework.response import Response

from weather.utils.city_id_list import CITY_ID_LIST
from weather.models import WeatherInfo, WeatherRequest

from application.adapters import OpenWeatherAdpter


class CollectWeatherUseCase:

    def __init__(self, weather_request: WeatherRequest, weather_consumer = OpenWeatherAdpter()) -> None:
        self.weather_request = weather_request
        self.weather_consumer = weather_consumer

    def execute(self):
        asyncio.run(self._process())

    async def _process(self):
        tasks = []
        for city_id in CITY_ID_LIST:
            task = asyncio.create_task(self._fetch_and_process(city_id))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def _fetch_and_process(self, city_id):
        response = await self.weather_consumer.execute(city_id)
        await self._process_response(response)

    async def _process_response(self, response: Response):
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
