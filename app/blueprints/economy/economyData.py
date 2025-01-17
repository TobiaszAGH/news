from datetime import timedelta
from data_visualization import generate_graph_html
from .functions import fetch_link


class economyData():
    def __init__(self):
        self.graph_data = {
            'x': [],
            'y': [],
            'label': ['Data', 'Kursy waluty w PLN'],
            'name': [],
            'index_y2': []
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
        codes, topCount = ['EUR', 'USD', 'CHF'], 7
        for code in codes:
            X, Y = [], []
            link = f'https://api.nbp.pl/api/exchangerates/rates/A/{code}/last/{topCount}/'
            x, y, name = fetch_link(link)
            X += x
            Y += y

            self.graph_data['x'] = X
            self.graph_data['y'].append(Y)
            self.graph_data['name'].append(name)
            self.graph_data['index_y2'].append(0)

    def fetch_api(self):
        for curr_code in self.curr_codes:
            if curr_code == 'Wybierz walutę':
                return
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

    def graph(self, leg=True):
        if self.graph_data['x']:
            return generate_graph_html(self.graph_data, len(self.graph_data['x']), leg)
        else:
            return 'Brak danych dotyczących tych walut i przedziału czasowego'
