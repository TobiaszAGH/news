import pytest
from flask import Flask
from flask.testing import FlaskClient
from blueprints.weather.weatherService import getCurrentWeather, getForecast
  # Zakładamy, że blueprint znajduje się w `app/blueprints/weather/routes.py`
import requests_mock
from datetime import datetime, timedelta


# Testowanie funkcji getCurrentWeather
def test_getCurrentWeather():
    city = "Krakow"
    country_code = "PL"
    api_response = {
        "weather": [{"icon": "10d", "main": "Rain", "description": "light rain"}],
        "main": {"temp": 18.3, "feels_like": 17.5, "humidity": 82, "pressure": 1012},
        "sys": {"country": "PL"},
        "rain": {"1h": 1.5},
        "name": "Krakow"
    }

    with requests_mock.Mocker() as mocker:
        mocker.get(f'https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&lang=pl&units=metric&appid=57e63f42559d5a1388381afa287e4a1b',
                   json=api_response)
        result = getCurrentWeather(city, country_code)

    assert result is not None
    assert result['city'] == "Krakow"
    assert result['temp'] == 18.5  # Zaokrąglenie do połówek


# Testowanie funkcji getForecast
def test_getForecast():
    current_time = datetime.now()
    future_time = current_time + timedelta(hours=3)
    timestamp = int(future_time.timestamp())
    future_time_str = future_time.strftime("%Y-%m-%d %H:%M:%S")
    city = "Krakow"
    country_code = "PL"

    print(timestamp, future_time)
    api_response = {
  "cod": "200",
  "message": 0,
  "cnt": 40,
  "list": [
    {
      "dt": timestamp,
      "main": {
        "temp": 1.14,
        "feels_like": -1.86,
        "temp_min": 0.24,
        "temp_max": 1.14,
        "pressure": 1032,
        "sea_level": 1032,
        "grnd_level": 999,
        "humidity": 72,
        "temp_kf": 0.9
      },
      "weather": [
        {
          "id": 804,
          "main": "Clouds",
          "description": "zachmurzenie duże",
          "icon": "04n"
        }
      ],
      "clouds": {
        "all": 100
      },
      "wind": {
        "speed": 2.7,
        "deg": 266,
        "gust": 5.01
      },
      "visibility": 10000,
      "pop": 0,
      "sys": {
        "pod": "n"
      },
      "dt_txt": future_time_str
    }]}

    with requests_mock.Mocker() as mocker:
        mocker.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city},{country_code}&lang=pl&units=metric&appid=57e63f42559d5a1388381afa287e4a1b',
                   json=api_response)
        result = getForecast(city, country_code)
    
    print(result)  # Debugowanie
    assert result is not None
    assert len(result) > 0
    assert result[0][0]['temp'] == 1.0






# Testowanie endpointu '/weather'
def test_hello_endpoint(client: FlaskClient):
    # with client:
        response = client.post('/weather/', data={"city1": "Gdynia", "city2": "Warszawa", "city3": "Osl7o", "city4": "57))"})
        print(response.data) 
        assert response.status_code == 200
        assert b"Gdynia" in response.data
        assert b"Warszawa" in response.data
        assert b"Oslo" in response.data
        assert b"57))" not in response.data



  