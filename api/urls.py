from django.urls import path
from .views import SearchHistoryAPIView

app_name = "api"

urlpatterns = [
    path('history/', SearchHistoryAPIView.as_view(), name='search-history'),
]
