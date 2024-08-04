from django.contrib import admin

from weather.models import WeatherRequest, WeatherInfo


@admin.register(WeatherRequest)
class WeatherRequestAdmin(admin.ModelAdmin):
    list_display = ["request_id"]
    search_fields = ["request_id"]


@admin.register(WeatherInfo)
class WeatherInfoAdmin(admin.ModelAdmin):
    list_display = ["weather_request", "city_id", "weather_data"]
    search_fields = ["weather_request", "city_id"]
