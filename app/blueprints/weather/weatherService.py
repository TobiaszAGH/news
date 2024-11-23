import requests
import geocoder
from datetime import datetime, date
import math

key = '57e63f42559d5a1388381afa287e4a1b'

def round_to_half(x):
    return round(x * 2) / 2

def getCurrentWeather(city, country_code):
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&lang=pl&units=metric&appid={key}')

    if response.status_code == 200:
        data = response.json() 
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
        dataa = None

    return dataa


def getForecast(city, country_code):


    response = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city},{country_code}&lang=pl&units=metric&appid={key}')

    if response.status_code == 200:
        data = response.json()
        data = data['list']

        result = []
        today = {}
        result.append(today)

        daily = {
            'max_temp': float('-inf'),
            'min_temp': float('inf'),
            'pressure': 0,
            'humidity': 0,
            'rain': 0,
            'snow': 0,
            'icon': '',
            'description': ''
        }

        date_check = date.today()
        counter = -1
        for i in range(len(data)):

            step = data[i]
            dt = datetime.fromtimestamp(step['dt'])

            if date.today() == dt.date():
                today.update(
                    {step['dt_txt'] : {
                        'time': step['dt_txt'],
                        'temp': step['main']['temp'],
                        'feels_like' : step['main']['feels_like'],
                        'pressure': step['main']['pressure'],
                        'humidity': step['main']['humidity'],
                        'description': step['weather'][0]['description'],
                        'icon': step['weather'][0]['icon'],
                        'wind': step['wind']['speed'],
                        'rain': (step['rain']['3h']) if 'rain' in step else 0,
                        'snow': (step['snow']['3h']) if 'rain' in step else 0
                    }})
            else:
                if counter == -1:
                    date_check = dt.date()

                if date_check < dt.date():
                    
                    result.append({
                        'date': data[i-1]['dt_txt'],
                        'max_temp': round_to_half(daily['max_temp']),
                        'min_temp': round_to_half(daily['min_temp']),
                        'pressure': round(daily['pressure']/counter),
                        'humidity': round(daily['humidity']/counter),
                        'rain': daily['rain'],
                        'snow': daily['snow'],
                        'icon' : daily['icon'],
                        'description': daily['description']
                    })
                    counter = 0
                    daily = {
                        'max_temp': 0,
                        'min_temp': 0,
                        'pressure': 0,
                        'humidity': 0,
                        'rain': 0,
                        'snow': 0
                    }
                    date_check = dt.date()
               
                counter += 1
                daily['max_temp'] = step['main']['temp'] if step['main']['temp'] > daily['max_temp'] else daily['max_temp']
                daily['min_temp'] = step['main']['temp'] if step['main']['temp'] < daily['min_temp'] else daily['min_temp']
                daily['pressure'] += step['main']['pressure']
                daily['humidity'] += step['main']['humidity']
                if 'rain' in step:
                    daily['rain'] += step['rain']['3h']
                if 'snow' in step:
                    daily['snow'] += step['snow']['3h']

                if dt.time().hour >= 12 and dt.time().hour <= 14:
                    daily['icon'] = step['weather'][0]['icon']
                    daily['description'] = step['weather'][0]['description']
                 
        return result
    
    else:
        print(f"Error: {response.status_code}")
        return None