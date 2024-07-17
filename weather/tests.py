import unittest
from importlib import import_module
from unittest.mock import patch
from django.test import Client

from django.conf import settings
from django.contrib.messages.storage import session
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from weather.views import WeatherView
from weather.forms import CityForm
from django.urls import reverse

from requests import HTTPError

from .exeptions import CityNotFoundException
from .models import SearchHistory
from .service import get_coordinates_by_city, get_weather_data, update_search_history


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


class GetWeatherDataTest(unittest.TestCase):

    def test_get_weather_data(self):
        """Test case for existing city"""
        city = 'Moscow'
        weather_data = get_weather_data(city)

        self.assertIn('current', weather_data)
        self.assertIn('daily', weather_data)
        self.assertIn('time', weather_data['current'])
        self.assertIsInstance(weather_data['daily']['time'], list)
        self.assertEqual(len(weather_data['daily']['time']), 7)  # Assuming daily forecast has 7 days

    def test_get_weather_data_city_not_found(self):
        """Test case for non-existent city"""
        with self.assertRaises(CityNotFoundException):
            get_weather_data('NonExistentCity')

    def test_get_coordinates_by_city_not_found(self):
        """Test case for non-existent city in get_coordinates_by_city"""
        with self.assertRaises(CityNotFoundException):
            get_coordinates_by_city('fdsatr43')


class SearchHistoryUpdateTestCase(TestCase):
    def setUp(self):
        self.session_key = "test_session_key"
        self.city = "TestCity"

    def test_update_search_history(self):
        SearchHistory.objects.create(session_key=self.session_key, city=self.city, search_count=0)

        update_search_history(self.session_key, self.city)
        search_history = SearchHistory.objects.get(session_key=self.session_key, city=self.city)
        self.assertEqual(search_history.search_count, 1)

    def test_update_search_history_new_entry(self):

        update_search_history(self.session_key, self.city)
        search_history = SearchHistory.objects.get(session_key=self.session_key, city=self.city)

        self.assertIsNotNone(search_history)
        self.assertEqual(search_history.search_count, 1)


class WeatherViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_weather_view_post_valid_form(self):
        url = reverse('weather:weather_main')
        response = self.client.post(url, {'city': 'New York'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertIsInstance(response.context['form'], CityForm)
        self.assertIsNotNone(response.context.get('weather_data'))


