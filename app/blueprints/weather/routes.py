from flask import Flask, render_template, request, Blueprint
import requests
import geocoder
from .weatherService import getCurrentWeather, getForecast
import json

weather_bp = Blueprint(
    'weather_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)

# def get_country_code(city_name):
#     g = geocoder.osm(city_name)
#     if g.ok:
#         return g.country_code
#     else:
#         return None



@weather_bp.route('/', methods=['GET', 'POST'])
def hello():
    cities = []
    if request.form.get('city1'):
        if request.form.get('city1').lower() == 'dupa':
            cities.append('Warszawa')
        else:
            cities.append(request.form.get('city1'))
    if request.form.get('city2'):
        cities.append(request.form.get('city2'))
    if request.form.get('city3'):
        cities.append(request.form.get('city3'))
    if request.form.get('city4'):
        cities.append(request.form.get('city4'))
    if request.form.get('city5'):
        cities.append(request.form.get('city5'))
    data = []
    forecast = []
    i=0

    if len(cities) == 0:
        cities.append('Kraków')
    for city in cities:
        if getCurrentWeather(city, None) is not None:
            data.append(getCurrentWeather(city, None))
            forecast.append(getForecast(city, None))
        i += 1
      
    return render_template('weather_test.html', data = data, forecast = forecast)

@weather_bp.route('/widget')
def showWidget():
    data = getCurrentWeather("Kraków", "PL")

    return render_template('weather.html', data = data)


@weather_bp.route('/test')
def showdata():
    data = getCurrentWeather("Kraków", "PL")
    forecast = getForecast("Kraków", "PL")
    return json.dumps({'data': forecast})