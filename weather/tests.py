from unittest.mock import patch

import requests_mock
from django.test import TestCase

from requests import HTTPError

from .exeptions import CityNotFoundException
from .service import get_coordinates_by_city, get_weather_data


class TestGetCoordinatesByCity(TestCase):

    @patch('requests.get')
    def test_get_coordinates_by_city(self, mock_get):
        """Mock data"""
        mock_data = {
            'results': [
                {'lat': '55.7505412', 'lon': '37.6174782'}
            ]
        }
        mock_get.return_value.json.return_value = mock_data
        mock_get.return_value.raise_for_status.return_value = None

        """Test case for a valid city"""
        city = "Moscow"
        expected_coordinates = [55.7505412, 37.6174782]
        coordinates = get_coordinates_by_city(city)
        self.assertEqual(coordinates, expected_coordinates)

        """Test case for a invalid city"""
        mock_get.return_value.json.return_value = {}
        with self.assertRaises(CityNotFoundException):
            get_coordinates_by_city("34hkhf@#")

        """Test case for HTTPError from the API"""
        mock_get.return_value.raise_for_status.side_effect = HTTPError("404 Client Error")
        with self.assertRaises(HTTPError):
            get_coordinates_by_city(city)


class GetWeatherDataTest(TestCase):

    def test_get_weather_data(self):
        city = "Москва"
        mock_coordinates = [55.75, 37.625]

        # Mocking get_coordinates_by_city
        with patch('weather.service.get_coordinates_by_city') as mock_get_coordinates_by_city:
            mock_get_coordinates_by_city.return_value = mock_coordinates

            # Mocking the weather API response
            with requests_mock.Mocker() as mock_request:
                mock_request.get(requests_mock.ANY, json=self.mock_weather_data())

                # Call the function
                weather_data = get_weather_data(city)

                # Assertions
                self.assertEqual(weather_data['latitude'], 55.75)
                self.assertEqual(weather_data['longitude'], 37.625)
                self.assertIn('current', weather_data)
                self.assertIn('daily', weather_data)

    def mock_weather_data(self):
        # Mock dynamic weather data here based on your API response structure
        return {
            'latitude': 55.75,
            'longitude': 37.625,
            'current': {
                'temperature_2m': 30.9,
                'relative_humidity_2m': 31,
                'apparent_temperature': 31.7,
                'wind_speed_10m': 2.2
            },
            'daily': {
                'temperature_2m_max': [31.0, 28.6, 26.1, 26.3, 25.1, 25.3, 24.9],
                'apparent_temperature_max': [32.0, 29.4, 25.9, 25.5, 24.9, 25.7, 25.0],
                'precipitation_probability_max': [19, 71, 65, 55, 87, 55, 68],
                'wind_speed_10m_max': [5.8, 9.1, 7.9, 8.6, 6.5, 7.2, 8.0]
            }
        }
