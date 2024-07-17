from rest_framework import serializers
from weather.models import SearchHistory


class SearchHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchHistory
        fields = ('city', 'search_count')
