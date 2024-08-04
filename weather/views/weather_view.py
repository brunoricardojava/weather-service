from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from weather.serializers import WeatherRequestSerializer, GetWeatherRequestSerializer
from weather.models import WeatherInfo
from weather.utils.city_id_list import CITY_ID_LIST

from application.use_cases import CollectWeatherUseCase


class WeatherView(APIView):
    def post(self, request: Request, request_id: int) -> Response:
        try:
            data = {"request_id": request_id}
            serializer = WeatherRequestSerializer(data=data)
            if serializer.is_valid():
                weather_request = serializer.save()
                CollectWeatherUseCase(weather_request).execute()
                return Response({"Response": "All OK. S2"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            weather_request.delete()
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request: Request, request_id: int) -> Response:
        try:
            data = {"request_id": request_id}
            serializer = GetWeatherRequestSerializer(data=data)
            if serializer.is_valid():
                count_weather_infos = WeatherInfo.objects.filter(weather_request__request_id=request_id).count()
                total_percente = (count_weather_infos*100)/len(CITY_ID_LIST)
                return Response({"Total Percent": int(total_percente)}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
