from flask import render_template, request, Blueprint
from .weatherService import getCurrentWeather, getForecast
import re

# Utworzenie Blueprint
weather_bp = Blueprint(
    'weather_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)


# Usunięcie wprowadzonych przez użytkownika znaków specjalnych
def clean_city_name(city_name):

    # Pozwól na litery alfabetu łacińskiego, spacje i myślniki
    cleaned_name = re.sub(
        r"[^a-zA-ZąćęłńóśźżÄÖÜäöüßÇÉÈÊËéèêëÎÏîïÑñÓÒÔÖÕóòôöõÚÙÛÜúùûüŸÿ \-]", "",
        city_name
    )
    return cleaned_name.strip()


# Strona pogody
@weather_bp.route('/', methods=['GET', 'POST'])
def hello():
    cities = []
    # Pobieranie danych z formularza i ich walidacja
    if request.form.get('city1'):
        cities.append(clean_city_name(request.form.get('city1')))
    if request.form.get('city2'):
        cities.append(clean_city_name(request.form.get('city2')))
    if request.form.get('city3'):
        cities.append(clean_city_name(request.form.get('city3')))
    if request.form.get('city4'):
        cities.append(clean_city_name(request.form.get('city4')))
    if request.form.get('city5'):
        cities.append(clean_city_name(request.form.get('city')))
    data = []
    forecast = []
    i = 0

    # Co jeśli nie ma danych
    if len(cities) == 0:
        cities.append('Kraków')

    # Wywoływanie metod sprawdzających aktualną pogodę i prognoze
    for city in cities:
        # Sprawdzenie czy API coś zwróciło (czy miasto istnieje)
        if getCurrentWeather(city, None) is not None:
            data.append(getCurrentWeather(city, None))
            forecast.append(getForecast(city, None))
        i += 1

    # Renderowanie html
    return render_template('weather_page.html', data=data, forecast=forecast)


# Wyświetlanie preview na stronie głównej dla Krakowa
@weather_bp.route('/widget')
def showWidget():
    data = getCurrentWeather("Kraków", "PL")
    return render_template('weather.html', data=data)
