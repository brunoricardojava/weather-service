from pydantic import BaseModel


class WeatherInfoEntity(BaseModel):
    city_id: int
    temperature: float
    humidity: float
