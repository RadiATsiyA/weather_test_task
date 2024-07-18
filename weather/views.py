from django.shortcuts import render
from django.views import View

from .forms import CityForm
from .service import get_weather_data, update_search_history, get_session_key


class WeatherView(View):
    form_class = CityForm
    template_name = "weather/weather.html"

    def get(self, request):
        last_city = request.session.get('last_city')
        initial_data = {'city': last_city} if last_city else None
        form = self.form_class(initial=initial_data)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        weather_data = None
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = get_weather_data(city)

            session_key = get_session_key(request)
            request.session['last_city'] = city
            update_search_history(session_key, city)
        return render(request, self.template_name, {'form': form, 'weather_data': weather_data, 'city': city})

