from flask import Blueprint, render_template, request
from .forms import EconomyForm
import requests
from datetime import timedelta
import json
from data_visualization import generate_graph_html

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
        return render_template('economy.html', form=form, page='economy_bp.index')
    
    data_economy = {
        'x' : [],
        'y' : [],
        'label': ['Data', 'Kursy waluty w PLN'],
        'name': [],
        'index_y2' : []
    }
    
    curr_codes = [form.currency1.data, form.currency2.data, form.currency3.data]
    startdate = form.startdate.data
    todate = form.todate.data
    if startdate > todate:
        return 'Start musi być wcześniej niż koniec'
    if todate - startdate > timedelta(days=93):
        return 'Zakres nie może przekraczać 93 dni'
    for curr_code in curr_codes:
        if curr_code != 'Wybierz walutę':
            link = f'https://api.nbp.pl/api/exchangerates/rates/A/{curr_code}/{startdate}/{todate}'
            response = requests.get(link)
            if response.status_code == 200:
                data = response.json()
                x = [rate['effectiveDate'] for rate in data['rates']]
                y = [rate['mid'] for rate in data['rates']]
                name = data['currency']
                data_economy['x'] = x
                data_economy['y'].append(y)
                data_economy['name'].append(name)
                data_economy['index_y2'].append(0)
            else:
                print(response.status_code)
                print(link)
    graph=generate_graph_html(data_economy, len(data_economy['x']))

    return render_template('economy.html', form=form, graph=graph, page='economy_bp.index')