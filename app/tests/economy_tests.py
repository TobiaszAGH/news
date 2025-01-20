from flask.testing import FlaskClient
from blueprints.economy.economyData import fetch_link

from datetime import datetime, timedelta

# unit tests
def test_economy_data_load(economy_data):
    curr_codes = ['USD', 'EUR']
    startdate = datetime.strptime('2024-11-12', '%Y-%m-%d').date()
    todate = datetime.strptime('2024-12-14', '%Y-%m-%d').date()
    last_date = datetime.strptime('2024-12-16', '%Y-%m-%d').date()
    test_ed = economy_data
    test_ed.load(curr_codes, startdate, todate, last_date)
    assert test_ed.curr_codes == curr_codes
    assert test_ed.dates == [ (startdate, todate) ]

def test_economy_data_load_swapped_dates(economy_data):
    curr_codes = ['USD', 'EUR']
    todate = datetime.strptime('2024-11-12', '%Y-%m-%d').date()
    startdate = datetime.strptime('2024-12-14', '%Y-%m-%d').date()
    last_date = datetime.strptime('2024-12-16', '%Y-%m-%d').date()
    test_ed = economy_data
    test_ed.load(curr_codes, startdate, todate, last_date)
    assert test_ed.curr_codes == curr_codes
    assert test_ed.dates == [ (todate, startdate) ]

def test_economy_data_load_long_period(economy_data):
    curr_codes = ['USD', 'EUR']
    startdate = datetime.strptime('2022-11-12', '%Y-%m-%d').date()
    todate = datetime.strptime('2024-12-14', '%Y-%m-%d').date()
    last_date = datetime.strptime('2024-12-16', '%Y-%m-%d').date()
    test_ed = economy_data
    test_ed.load(curr_codes, startdate, todate, last_date)
    assert test_ed.curr_codes == curr_codes
    assert test_ed.dates[0][0] == startdate
    assert test_ed.dates[-1][-1] == todate
    for date in test_ed.dates:
        assert date[1] - date[0] <= timedelta(days=93)

def test_economy_data_default(economy_data):
    test_ed = economy_data
    test_ed.default()
    assert test_ed.graph_data['x']
    assert test_ed.graph_data['y']
    assert test_ed.graph_data['name']
    assert test_ed.graph_data['index_y2']

def test_economy_data_fetch_api(economy_data):
    curr_codes = ['USD', 'EUR']
    startdate = datetime.strptime('2024-11-12', '%Y-%m-%d').date()
    todate = datetime.strptime('2024-12-14', '%Y-%m-%d').date()
    last_date = datetime.strptime('2024-12-16', '%Y-%m-%d').date()
    test_ed = economy_data
    test_ed.load(curr_codes, startdate, todate, last_date)
    test_ed.fetch_api()
    assert test_ed.graph_data['x']
    assert test_ed.graph_data['y']
    assert test_ed.graph_data['name']
    assert test_ed.graph_data['index_y2']

def test_fetch_link():
    link ='https://api.nbp.pl/api/exchangerates/rates/A/EUR/last/6/'
    x, y, name = fetch_link(link)
    assert len(x) == 6
    assert len(y) == 6
    assert name == 'euro'

# integration test
def test_economy_endpoint(client: FlaskClient):
    with client:
        response = client.get('/economy/')
        print(response.data) 
        assert response.status_code == 200

def test_start_after_end(client: FlaskClient):
    with client:
        response = client.post('/economy/', data={'startdate': '2024-11-11', 'todate': '2024-10-10', 'currency1': 'USD'})
        assert response.status_code == 200

def test_correct_economy(client: FlaskClient):
    with client:
        response = client.post('/economy/', data={'startdate': '2024-11-11', 'todate': '2024-12-12', 'currency1': 'USD'})
        assert response.status_code == 200

def test_over_93_days(client: FlaskClient):
    with client:
        response = client.post('/economy/', data={'startdate': '2024-01-11', 'todate': '2024-10-10', 'currency1': 'USD'})
        assert response.status_code == 200

