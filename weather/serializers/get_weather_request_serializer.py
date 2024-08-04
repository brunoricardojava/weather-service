from rest_framework import serializers
from rest_framework.serializers import ValidationError

from weather.models import WeatherRequest


class GetWeatherRequestSerializer(serializers.Serializer):
    request_id = serializers.IntegerField()

    def validate_request_id(self, request_id):
        if not WeatherRequest.objects.filter(request_id=request_id).exists():
            raise ValidationError(f"WeatherRequest with id: {request_id} does not exist.")
        return request_id
