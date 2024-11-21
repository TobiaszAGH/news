from flask import Flask, render_template, request, Blueprint
import requests
import geocoder

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
          

    key = '57e63f42559d5a1388381afa287e4a1b'
    city = 'Warszawa'
    country_code = 'PL'

    if request.form.get('city'):
        city = request.form.get('city')
        country_code = get_country_code(city)

    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&lang=pl&units=metric&appid={key}')

    if response.status_code == 200:
        data = response.json() 
        print(data['weather'][0]['icon'])
        dataa = {
                'icon': data['weather'][0]['icon'],
                'main' : data['weather'][0]['main'],
                'description' : data['weather'][0]['description'],
                'temp' : data['main']['temp'],
                'feeltemp': data['main']['feels_like'],
                'humidity' : data['main']['humidity'],
                'pressure' : data['main']['pressure'],
                'city' : data['name'],
                'country' : data['sys']['country']  
            }

        if(data.get('rain', 0) == 0):
            dataa['rain'] = 0
        else:
            dataa['rain'] = data['rain']['1h']
            print(dataa.get('icon', 0))
    else:
        data = 0

      
    return render_template('weather.html', data = dataa)