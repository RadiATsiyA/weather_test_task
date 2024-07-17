import requests
from django.shortcuts import render
from django.views import View

from .forms import CityForm
from .service import get_weather_data


class WeatherView(View):
    form_class = CityForm
    template_name = "weather/weather.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        weather_data = None
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = get_weather_data(city)
        return render(request, self.template_name, {'form': form, 'weather_data': weather_data})

