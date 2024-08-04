from django.db import models

from .base_model import BaseModel
from .weather_request_model import WeatherRequest


class WeatherInfo(BaseModel):
    weather_request = models.ForeignKey(WeatherRequest, on_delete=models.CASCADE, db_index=True)
    city_id = models.IntegerField(db_index=True)
    weather_data = models.JSONField()
