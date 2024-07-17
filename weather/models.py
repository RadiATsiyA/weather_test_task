from django.contrib.auth.models import User
from django.db import models


class SearchHistory(models.Model):
    session_key = models.CharField(max_length=256)
    city = models.CharField(max_length=100)
    search_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.city} - {self.search_count} times"
