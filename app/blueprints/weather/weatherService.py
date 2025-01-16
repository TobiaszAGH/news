import requests
from datetime import datetime, date

key = '57e63f42559d5a1388381afa287e4a1b'


def round_to_half(x):
    return round(x * 2) / 2


# Aktualna pogoda
def getCurrentWeather(city, country_code):
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&lang=pl&units=metric&appid={key}')

    # Jeśli kod 200
    if response.status_code == 200:
        data = response.json()
        # Dodanie potrzebnych danych do słownika
        dataa = {
                'icon': data['weather'][0]['icon'],
                'main': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                # Zaokrąglanie
                'temp': round_to_half(data['main']['temp']),
                # Zaokrąglanie
                'feeltemp': round_to_half(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'city': data['name'],
                'country': data['sys']['country']
            }
        # Sprawdzenie czy są opady śniegu i deszczu
        if (data.get('rain', 0) == 0):
            dataa['rain'] = 0
        else:
            dataa['rain'] = data['rain']['1h']
        if (data.get('snow', 0) == 0):
            dataa['snow'] = 0
        else:
            dataa['snow'] = data['snow']['1h']
    else:
        dataa = None  # brak danych - zwraca None

    return dataa


def getForecast(city, country_code):

    response = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city},{country_code}&lang=pl&units=metric&appid={key}')

    # Jeśli kod 200
    if response.status_code == 200:
        data = response.json()
        data = data['list']

        # utworzenie list do których pójdą dane
        result = []
        today = []
        result.append(today)

        # słownik na dane prognozowane
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

        date_check = date.today()  # sprawdzanie dnia
        counter = -1
        for i in range(len(data)):

            step = data[i]
            dt = datetime.fromtimestamp(step['dt'])

            # Sprawdzenie czy to dane na dziś
            if date.today() == dt.date():
                # dodanie prognozy na późniejsze godziny (ten sam dzień)
                today.append({
                        'time': step['dt_txt'],
                        # Zaokrąglanie
                        'temp': round_to_half(step['main']['temp']),
                        # Zaokrąglanie
                        'feels_like': round_to_half(step['main']['feels_like']),
                        'pressure': step['main']['pressure'],
                        'humidity': step['main']['humidity'],
                        'description': step['weather'][0]['description'],
                        'icon': step['weather'][0]['icon'],
                        'wind': step['wind']['speed'],
                        'rain': step.get('rain', {}).get('3h', 0),
                        'snow': step.get('snow', {}).get('3h', 0)
                    })
            else:
                # jeśli nie było danych na następne godziny (np o godz 23)
                if counter == -1:
                    date_check = dt.date()
                    counter = 0

                # jeśli koniec analizy całego dnia
                if date_check < dt.date():
                    # zapisanie wyników
                    result.append({
                        'date': data[i-1]['dt_txt'],
                        # zaokrąglanie
                        'max_temp': round_to_half(daily['max_temp']),
                        # zaokrąglanie
                        'min_temp': round_to_half(daily['min_temp']),
                        # średine ciśnienie
                        'pressure': round(daily['pressure']/counter),
                        # średnia wilgotniść
                        'humidity': round(daily['humidity']/counter),
                        'rain': round(daily['rain'], 2),
                        'snow': round(daily['snow'], 2),
                        'icon': daily['icon'],
                        'description': daily['description']
                    })

                    # czyszczenie słownika i zmiana dnia
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
                # Wydobywanie największej i najmniejszej temp danego dnia
                daily['max_temp'] = step['main']['temp'] if step['main']['temp'] > daily['max_temp'] else daily['max_temp']
                daily['min_temp'] = step['main']['temp'] if step['main']['temp'] < daily['min_temp'] else daily['min_temp']
                # Sumowanie ciśnienia i wilgotności (do obliczenia średniej)
                daily['pressure'] += step['main']['pressure']
                daily['humidity'] += step['main']['humidity']

                # Sprawdzenie czy są opady i sumowanie ich
                if 'rain' in step:
                    daily['rain'] += step['rain']['3h']
                if 'snow' in step:
                    daily['snow'] += step['snow']['3h']
                # wybór ikony i opisu ze środka danego dnia
                if dt.time().hour >= 12 and dt.time().hour <= 14:
                    daily['icon'] = step['weather'][0]['icon']
                    daily['description'] = step['weather'][0]['description']

        return result
    else:
        print(f"Error: {response.status_code}")
        return None  # brak danych zwraca None
