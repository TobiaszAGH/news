import requests
import geocoder
from datetime import datetime, date
import math

key = '57e63f42559d5a1388381afa287e4a1b'

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
        
        forecast_data = {
            'short': [],
            'dzien1': [],
            'dzien2': [],
            'dzien3': [],
            'dzien4': [],
            'dzien5': []
        }
        
        current_day = date.today()
        day_counter = 0

        # List to store middle forecasts for dzien2, dzien3, dzien4, dzien5
        middle_forecasts = []

        for entry in data:
            dt = datetime.fromtimestamp(entry['dt'])
            forecast = {
                'icon': entry['weather'][0]['icon'],
                'main': entry['weather'][0]['main'],
                'description': entry['weather'][0]['description'],
                'temp': entry['main']['temp'],
                'feeltemp': entry['main']['feels_like'],
                'humidity': entry['main']['humidity'],
                'pressure': entry['main']['pressure'],
                'time': entry['dt_txt']
            }

            # Add forecast data to the appropriate day based on the date
            if dt.date() > current_day:
                current_day = dt.date()
                day_counter += 1

            if day_counter == 0:
                forecast_data['dzien1'].append(forecast)
            elif day_counter == 1:
                forecast_data['dzien2'].append(forecast)
            elif day_counter == 2:
                forecast_data['dzien3'].append(forecast)
            elif day_counter == 3:
                forecast_data['dzien4'].append(forecast)
            elif day_counter == 4:
                forecast_data['dzien5'].append(forecast)

        # Now select the middle of each day's forecast starting from dzien2
        for dzien in ['dzien2', 'dzien3', 'dzien4', 'dzien5']:
            day_data = forecast_data[dzien]
            if day_data:  # Ensure there is data for this day
                middle_index = len(day_data) // 2  # Choose the middle forecast
                middle_forecasts.append(day_data[middle_index])

        # Add middle forecasts to the 'short' list
        forecast_data['short'] = middle_forecasts

        # You can remove this print in production

        return forecast_data
    else:
        print(f"Error: {response.status_code}")
        return None