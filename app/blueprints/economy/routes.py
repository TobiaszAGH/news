from flask import Blueprint, render_template, request, flash
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

class economyData():
    def __init__(self):
        self.graph_data = {
            'x' : [],
            'y' : [],
            'label': ['Data', 'Kursy waluty w PLN'],
            'name': [],
            'index_y2' : []
        }

    def load(self, curr_codes, startdate, todate):
        self.curr_codes = curr_codes

        # switch dates if in wrong order
        if startdate > todate: 
            todate, startdate = startdate, todate
        
        # split into smaller periods if selected period is longer than api limit (93 days)
        self.dates = []
        while todate - startdate > timedelta(days=93):
            new_startdate = startdate + timedelta(days=93)
            self.dates.append((startdate, new_startdate))
            startdate = new_startdate + timedelta(days=1)
        self.dates.append((startdate, todate))
        


    def default(self):
        codes, topCount = ['EUR','USD',"CHF"], 7
        for code in codes:
            X, Y = [], []
            link =f"https://api.nbp.pl/api/exchangerates/rates/A/{code}/last/{topCount}/"
            x, y, name = fetch_link(link)
            X += x
            Y += y
                    
            self.graph_data['x'] = X
            self.graph_data['y'].append(Y)
            self.graph_data['name'].append(name)
            self.graph_data['index_y2'].append(0)

    def fetch_api(self):
        for curr_code in self.curr_codes:
            if curr_code != 'Wybierz walutę':
                X, Y = [], []

                for startdate, todate in self.dates:
                    link = f'https://api.nbp.pl/api/exchangerates/rates/A/{curr_code}/{startdate}/{todate}'
                    x, y, name = fetch_link(link)
                    X += x
                    Y += y
                    
                self.graph_data['x'] = X
                self.graph_data['y'].append(Y)
                self.graph_data['name'].append(name)
                self.graph_data['index_y2'].append(0)

    def graph(self):
        return generate_graph_html(self.graph_data, len(self.graph_data['x']))

    
def fetch_link(link):
    response = requests.get(link)
    if response.status_code == 200:
        data = response.json()
        x = [rate['effectiveDate'] for rate in data['rates']]
        y = [rate['mid'] for rate in data['rates']]
        name = data['currency']
    return (x,y,name)

@economy_bp.route('/', methods=['GET','POST'])
def index():
    form = EconomyForm()
    
    if request.method == 'GET':
        economy_data = economyData()
        economy_data.default()
        graph = economy_data.graph()
        return render_template('economy.html', form=form, graph=graph, page='economy_bp.index')
    
    # load data from form
    curr_codes = [form.currency1.data, form.currency2.data, form.currency3.data]
    startdate = form.startdate.data
    todate = form.todate.data

    economy_data = economyData()
    economy_data.load(curr_codes, startdate, todate)
    economy_data.fetch_api()
    graph=economy_data.graph()

    return render_template('economy.html', form=form, graph=graph, page='economy_bp.index')

@economy_bp.route('/preview')
def preview():
    economy_data = economyData()
    economy_data.default()
    return'<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>' + economy_data.graph()