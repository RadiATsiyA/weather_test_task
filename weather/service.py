from datetime import datetime

from django.conf import settings
import requests
from .exeptions import CityNotFoundException
from .models import SearchHistory


def update_search_history(session_key, city: str) -> None:
    search_history, created = SearchHistory.objects.get_or_create(session_key=session_key, city=city)
    search_history.search_count += 1
    search_history.save()


def get_coordinates_by_city(city: str) -> list[float, float]:
    url = f'https://api.geoapify.com/v1/geocode/search?text={city}&format=json&apiKey={settings.GEOCODE_API}'

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if not data or not data.get('results'):
        raise CityNotFoundException(f"No data found for the city: {city}")

    coordinates = [float(data['results'][0]['lat']), float(data['results'][0]['lon'])]
    return coordinates


def get_weather_data(city: str):
    coordinates = get_coordinates_by_city(city)
    latitude = coordinates[0]
    longitude = coordinates[1]

    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}" \
              f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m" \
              f"&daily=temperature_2m_max,apparent_temperature_max,precipitation_probability_max,wind_speed_10m_max" \
              f"&timezone=Europe%2FMoscow"

    response = requests.get(api_url)
    response.raise_for_status()
    weather_data = response.json()
    formatted_weather_data = format_weather_data(weather_data)
    return formatted_weather_data


def format_weather_data(weather_data):
    weather_data['current']['time'] = format_date(weather_data['current']['time'])
    weather_data['daily']['time'] = [format_date(date) for date in weather_data['daily']['time']]
    return weather_data


def format_date(date_str):
    date_obj = datetime.fromisoformat(date_str.replace('T', ' '))
    formatted_date = date_obj.strftime("%d.%m, %a")
    return formatted_date

