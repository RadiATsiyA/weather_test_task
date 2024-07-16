
from django.conf import settings
import requests
from .exeptions import CityNotFoundException, ErrorFetchingData


def get_coordinates_by_city(city: str) -> list[float, float]:
    url = f'https://api.geoapify.com/v1/geocode/search?text={city}&format=json&apiKey={settings.GEOCODE_API}'

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if data:
        coordinates = [float(data['results'][0]['lat']), float(data['results'][0]['lon'])]
        return coordinates
    else:
        raise CityNotFoundException(f"No data found for the city: {city}")


def get_weather_data(city: str):
    coordinates = get_coordinates_by_city(city)
    latitude = coordinates[0]
    longitude = coordinates[1]

    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}" \
              f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m" \
              f"&daily=temperature_2m_max,apparent_temperature_max,precipitation_probability_max,wind_speed_10m_max" \
              f"&timezone=Europe%2FMoscow"

    # api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}" \
    #           f"&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

