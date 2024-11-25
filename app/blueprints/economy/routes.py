from flask import Blueprint, render_template, request
from .forms import EconomyForm
import requests
from datetime import timedelta
import json

economy_bp = Blueprint(
    'economy_bp',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@economy_bp.route('/', methods=['GET','POST'])
def index():
    form = EconomyForm()
    if request.method == 'GET':
        return render_template('economy.html', form=form)
    
    curr_codes = [form.currency1.data, form.currency2.data, form.currency3.data]
    startdate = form.startdate.data
    todate = form.todate.data
    if startdate > todate:
        return 'Start musi być wcześniej niż koniec'
    if todate - startdate > timedelta(days=93):
        return 'Zakres nie może przekraczać 93 dni'
    data = json.loads('{"currencies": []}')
    for curr_code in curr_codes:
        if curr_code != 'Wybierz walutę':
            link = f'https://api.nbp.pl/api/exchangerates/rates/A/{curr_code}/{startdate}/{todate}'
            response = requests.get(link)
            if response.status_code == 200:
                data["currencies"].append(response.json())
            else:
                print(response.status_code)
                print(link)

    return data