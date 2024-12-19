import pytest 
from app import app
from flask import Flask
import requests
from datetime import datetime, timedelta
from blueprints.calendar.routes import get_nameday, get_holiday, get_proverb, calendar_bp


@pytest.fixture
def client():
    app = Flask(__name__, template_folder='../templates')
    app.register_blueprint(calendar_bp, url_prefix = '/calendar', template_folder='templates')  
    app.config['TESTING'] = True
    return app.test_client()

#testy jednostkowe

#testy integracyjne
def test_get_nameday_successful_response(requests_mock):
    date_str = "2024-12-12"
    date = datetime.strptime(date_str, '%Y-%m-%d')
    mock_nameday_response = {
        "nameday": {
            "pl": "Jan, Maria"
        }
    }
    requests_mock.get(
        f"https://nameday.abalin.net/api/V1/getdate?day={date.day}&month={date.month}&country=pl",
        json=mock_nameday_response,
        status_code=200
    )
    result=get_nameday(date)
    assert result == ["Jan", "Maria"]

def test_get_nameday_no_nameday(requests_mock):
    date_str = "2024-12-12"
    date = datetime.strptime(date_str, '%Y-%m-%d')
    mock_nameday_response = {
        "nameday": {
            "pl": ""
        }
    }
    requests_mock.get(
        f"https://nameday.abalin.net/api/V1/getdate?day={date.day}&month={date.month}&country=pl",
        json = mock_nameday_response,
        status_code = 200
    )
    result = get_nameday(date)
    assert result == ["Brak imienin"]

def test_get_nameday_failed_response(requests_mock):
    date_str = "2024-12-12"
    date = datetime.strptime(date_str, '%Y-%m-%d')
    requests_mock.get(
        f"https://nameday.abalin.net/api/V1/getdate?day={date.day}&month={date.month}&country=pl",
        status_code=500
    )

    result, status_code = get_nameday(date)
    assert result == "Failed to retrieve data with status code 500"
    assert status_code == 500

def test_get_holiday_successful_response(requests_mock):
    date_str="2024-12-25"
    date=datetime.strptime(date_str, '%Y-%m-%d')
    mock_holiday_response = [
        {"name": "Boże Narodzenie"},
        {"name": "Drugi dzień Świąt"}
    ]
    requests_mock.get(
        f'https://pniedzwiedzinski.github.io/kalendarz-swiat-nietypowych/{date.month}/{date.day}.json',
        json = mock_holiday_response,
        status_code=200
    )
    result = get_holiday(date)
    assert result == ['Boże Narodzenie', 'Drugi dzień Świąt']

def test_get_holiday_no_holiday(requests_mock):
    date_str="2024-12-25"
    date=datetime.strptime(date_str, '%Y-%m-%d')
    mock_holiday_response = [
    ]
    requests_mock.get(
        f'https://pniedzwiedzinski.github.io/kalendarz-swiat-nietypowych/{date.month}/{date.day}.json',
        json = mock_holiday_response,
        status_code=200
    )
    result = get_holiday(date)
    assert result == ['Brak nazwy święta']

def test_get_holiday_failed_response(requests_mock):
    date_str="2024-12-25"
    date=datetime.strptime(date_str, '%Y-%m-%d')
    requests_mock.get(
        f"https://pniedzwiedzinski.github.io/kalendarz-swiat-nietypowych/{date.month}/{date.day}.json",
        status_code=404
    )

    result, status_code = get_holiday(date)
    assert result == "Failed to retrieve data with status code 404"
    assert status_code == 500

def test_get_proverb_successful_response(requests_mock):
    date_str="2024-12-25"
    date=datetime.strptime(date_str, '%Y-%m-%d')
    day = date.day
    month = date.month
    mock_html = '''<div class="calCard_proverb-content">
        „Gdy w grudniu mucha się pojawia, zima lekka bywa.” „Grudniowe przysłowia to mądrość ludowa.”
    </div>
    '''
    requests_mock.get(f"https://www.kalbi.pl/{day}-{month}", text=mock_html, status_code=200)

    result = get_proverb(day, month)
    assert result == [
        "Gdy w grudniu mucha się pojawia, zima lekka bywa.",
        "Grudniowe przysłowia to mądrość ludowa."
    ]
