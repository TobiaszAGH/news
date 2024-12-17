from flask import Blueprint, render_template, request, flash
from .forms import EconomyForm
import requests
from datetime import timedelta, datetime
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
            'label' : ['Data', 'Kursy waluty w PLN'], 
            'name' : [], 
            'index_y2' : []
        }

    def load(self, curr_codes, startdate, todate, last_date):
        self.curr_codes = curr_codes

        if startdate > last_date:
            startdate = last_date
        if todate > last_date:
            todate = last_date
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
                X, Y, name = [], [], ''

                for startdate, todate in self.dates:
                    link = f'https://api.nbp.pl/api/exchangerates/rates/A/{curr_code}/{startdate}/{todate}'
                    resp = fetch_link(link)
                    if resp:
                        x, y, name = resp
                        X += x
                        Y += y
                    
                self.graph_data['x'] = X
                self.graph_data['y'].append(Y)
                self.graph_data['name'].append(name)
                self.graph_data['index_y2'].append(0)

    def graph(self):
        if self.graph_data['x']:
            return generate_graph_html(self.graph_data, len(self.graph_data['x']))
        else:
            return 'Brak danych dotyczących tych walut i przedziału czasowego'

    
def fetch_link(link):
    response = requests.get(link)
    if response.status_code == 200:
        data = response.json()
        x = [rate['effectiveDate'] for rate in data['rates']]
        y = [rate['mid'] for rate in data['rates']]
        name = data['currency']
        return (x,y,name)
    else:
        print(response.status_code)
        print(link)
        return None
    

def get_current_codes_and_last_date():
    link = 'https://api.nbp.pl/api/exchangerates/tables/a'
    response = requests.get(link).json()[0]
    currencies = response['rates']
    curr_codes = ['Wybierz walutę'] + [curr['code'] for curr in currencies]
    last_date = datetime.strptime(response['effectiveDate'], '%Y-%m-%d').date()
    return curr_codes, last_date


@economy_bp.route('/', methods=['GET','POST'])
def index():
    available_curr_codes, last_date = get_current_codes_and_last_date()
    form = EconomyForm()
    form.currency1.choices = available_curr_codes
    form.currency2.choices = available_curr_codes
    form.currency3.choices = available_curr_codes
    
    
    if request.method == 'GET':
        form.currency1.default = 'Wybierz walutę'
        form.currency2.default = 'Wybierz walutę'
        form.currency3.default = 'Wybierz walutę'
        form.startdate.default = last_date - timedelta(days=7)
        form.todate.default = last_date
        form.process()

        economy_data = economyData()
        economy_data.default()
        graph = economy_data.graph()
        return render_template('economy.html', form=form, graph=graph, page='economy_bp.index')
    
    # load data from form
    curr_codes = [form.currency1.data, form.currency2.data, form.currency3.data]
    startdate = form.startdate.data
    todate = form.todate.data
    economy_data = economyData()
    economy_data.load(curr_codes, startdate, todate, last_date)
    economy_data.fetch_api()
    graph=economy_data.graph()

    return render_template('economy.html', form=form, graph=graph, page='economy_bp.index')
    

@economy_bp.route('/preview')
def preview():
    economy_data = economyData()
    economy_data.default()
    return'<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>' + economy_data.graph()