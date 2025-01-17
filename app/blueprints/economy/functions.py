import requests
from datetime import datetime


def get_current_codes_and_last_date():
    link = 'https://api.nbp.pl/api/exchangerates/tables/a'
    response = requests.get(link).json()[0]
    currencies = response['rates']
    curr_codes = ['Wybierz walutę'] + [curr['code'] for curr in currencies]
    last_date = datetime.strptime(response['effectiveDate'], '%Y-%m-%d').date()
    return curr_codes, last_date


def fetch_link(link):
    response = requests.get(link)
    if response.status_code == 200:
        data = response.json()
        x = [rate['effectiveDate'] for rate in data['rates']]
        y = [rate['mid'] for rate in data['rates']]
        name = data['currency']
        return (x, y, name)
    else:
        print(response.status_code)
        print(link)
        return None
