// Function to display current weather
function displayCurrentWeather(data) {
    const currentWeatherDiv = document.getElementById('current-weather');
    const currentWeatherHTML = `
        <div class="weather-card">
            <h5>Right now: ${data.current.time}</h5>
            <p><strong>Temperature:</strong> ${data.current.temperature_2m} ${data.current_units.temperature_2m}</p>
            <p><strong>Relative Humidity:</strong> ${data.current.relative_humidity_2m} ${data.current_units.relative_humidity_2m}</p>
            <p><strong>Apparent Temperature:</strong> ${data.current.apparent_temperature} ${data.current_units.apparent_temperature}</p>
            <p><strong>Wind Speed:</strong> ${data.current.wind_speed_10m} ${data.current_units.wind_speed_10m}</p>
        </div>
    `;
    currentWeatherDiv.innerHTML = currentWeatherHTML;
}

// Function to display daily weather
function displayDailyWeather(data) {
    const dailyWeatherDiv = document.getElementById('daily-weather');
    let dailyWeatherHTML = '';
    for (let i = 0; i < data.daily.time.length; i++) {
        dailyWeatherHTML += `
            <div class="weather-card">
                <h5>${data.daily.time[i]}</h5>
                <p><strong>Max Temperature:</strong> ${data.daily.temperature_2m_max[i]} ${data.daily_units.temperature_2m_max}</p>
                <p><strong>Apparent Max Temperature:</strong> ${data.daily.apparent_temperature_max[i]} ${data.daily_units.apparent_temperature_max}</p>
                <p><strong>Precipitation Probability:</strong> ${data.daily.precipitation_probability_max[i]} ${data.daily_units.precipitation_probability_max}</p>
                <p><strong>Max Wind Speed:</strong> ${data.daily.wind_speed_10m_max[i]} ${data.daily_units.wind_speed_10m_max}</p>
            </div>
        `;
    }
    dailyWeatherDiv.innerHTML = dailyWeatherHTML;
}

function displayWeatherData(weatherData) {
    displayCurrentWeather(weatherData);
    displayDailyWeather(weatherData);
}
