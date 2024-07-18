from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from rest_framework.test import APIClient
from weather.models import SearchHistory
from .serializers import SearchHistorySerializer


class SearchHistorySerializerTestCase(TestCase):

    def setUp(self):
        self.search_history_data = {
            'city': 'New York',
            'search_count': 5,
        }

        self.search_history = SearchHistory.objects.create(
            city=self.search_history_data['city'],
            search_count=self.search_history_data['search_count'],
        )

        self.serializer = SearchHistorySerializer(instance=self.search_history)

    def test_serializer_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'city', 'search_count'})

    def test_serializer_data(self):
        data = self.serializer.data
        self.assertEqual(data['city'], self.search_history_data['city'])
        self.assertEqual(data['search_count'], self.search_history_data['search_count'])

    def test_create_valid_serializer(self):
        serializer_data = {
            'city': 'Los Angeles',
            'search_count': 3,
        }
        serializer = SearchHistorySerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())
        search_history_obj = serializer.save()
        self.assertEqual(search_history_obj.city, serializer_data['city'])
        self.assertEqual(search_history_obj.search_count, serializer_data['search_count'])

