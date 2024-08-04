from django.db import models
from .base_model import BaseModel


class WeatherRequest(BaseModel):
    request_id = models.IntegerField(unique=True, db_index=True)

    def __str__(self) -> str:
        return str(self.request_id)
