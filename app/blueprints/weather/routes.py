from flask import Flask, render_template, request, Blueprint
import requests
import geocoder
from .weatherService import getCurrentWeather, getForecast


weather_bp = Blueprint(
    'weather_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)

def get_country_code(city_name):
    g = geocoder.osm(city_name)
    if g.ok:
        return g.country_code
    else:
        return None



@weather_bp.route('/', methods=['GET', 'POST'])
def hello():
          

    
    city = 'Kraków'
    country_code = 'PL'
    if request.form.get('city'):
        city = request.form.get('city')
        country_code = get_country_code(city)

        if city.lower() == "dupa":
            city = "Warszawa"
        
    data = getCurrentWeather(city, country_code)

    forecast = getForecast(city, country_code)
      
    return render_template('weather2.html', data = data, forecast = forecast)