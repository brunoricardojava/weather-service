from django.urls import re_path

from weather.views import WeatherView

urlpatterns = [
    re_path(r"weather/(?P<request_id>[0-9]+)?$", WeatherView.as_view(), name="WeatherRoute"),
]
