import pytest 
from app import app
from flask import Flask, url_for
from unittest.mock import patch
from datetime import datetime, timedelta
from blueprints.calendar.routes import get_nameday, get_holiday, get_proverb, get_agh_news, parse_date, calendar_bp


@pytest.fixture
def client():
    app = Flask(__name__, template_folder='../templates')
    app.register_blueprint(calendar_bp, url_prefix = '/calendar', template_folder='templates')  
    app.config['TESTING'] = True
    return app.test_client()


#testy jednostkowe
def test_get_nameday_successful_response():
    date_str = "2024-12-12"
    date = datetime.strptime(date_str, '%Y-%m-%d')
    mock_nameday_response = {
        "nameday": {
            "pl": "Jan, Maria"
        }
    }
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_nameday_response
        result = get_nameday(date)
        assert result == ["Jan", "Maria"]
        mock_get.assert_called_once_with(
            f"https://nameday.abalin.net/api/V1/getdate?day={date.day}&month={date.month}&country=pl"
        )

def test_get_nameday_no_nameday():
    date_str = "2024-12-12"
    date = datetime.strptime(date_str, '%Y-%m-%d')
    mock_nameday_response = {
        "nameday": {
            "pl": ""
        }
    }
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_nameday_response
        result = get_nameday(date)
        assert result == ["Brak imienin"]
        mock_get.assert_called_once_with(
            f"https://nameday.abalin.net/api/V1/getdate?day={date.day}&month={date.month}&country=pl"
        )

def test_get_nameday_failed_response():
    date_str = "2024-12-12"
    date = datetime.strptime(date_str, "%Y-%m-%d")

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 500
        result, status_code = get_nameday(date)
        assert result == ["Brak imienin"]
        assert status_code == 500

        mock_get.assert_called_once_with(
            f"https://nameday.abalin.net/api/V1/getdate?day={date.day}&month={date.month}&country=pl"
        )
   
def test_get_holiday_successful_response():
    date_str="2024-12-25"
    date=datetime.strptime(date_str, '%Y-%m-%d')

    mock_holiday_response = [
        {"name": "Boże Narodzenie"},
        {"name": "Drugi dzień Świąt"}
    ]

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_holiday_response
        result = get_holiday(date)
        assert result == ['Boże Narodzenie', 'Drugi dzień Świąt']

        mock_get.assert_called_once_with(
            f"https://pniedzwiedzinski.github.io/kalendarz-swiat-nietypowych/{date.month}/{date.day}.json"
        )
    
def test_get_holiday_no_response():
    date_str="2024-12-25"
    date=datetime.strptime(date_str, '%Y-%m-%d')

    mock_holiday_response = [
    ]

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_holiday_response
        result = get_holiday(date)
        assert result == ['Brak nazwy święta']

        mock_get.assert_called_once_with(
            f"https://pniedzwiedzinski.github.io/kalendarz-swiat-nietypowych/{date.month}/{date.day}.json"
        )

def test_holiday_failed_response():
    date_str = "2024-12-12"
    date = datetime.strptime(date_str, "%Y-%m-%d")

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 500
        result, status_code = get_holiday(date)
        assert result == ['Brak nazwy święta']
        assert status_code == 500

        mock_get.assert_called_once_with(
            f"https://pniedzwiedzinski.github.io/kalendarz-swiat-nietypowych/{date.month}/{date.day}.json"
        )


def test_get_proverb_successful_response():
    date_str="2024-12-25"
    date=datetime.strptime(date_str, '%Y-%m-%d')
    day = date.day
    month = date.month
    mock_html = '''<div class="calCard_proverb-content">
        „Przyslowie pierwsze” „Przyslowie drugie”
    </div>
    '''
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = mock_html.encode('utf-8')
        result = get_proverb(day, month)
        assert result == [
        "Przyslowie pierwsze",
        "Przyslowie drugie"]
        mock_get.assert_called_once_with("https://www.kalbi.pl/25-12")

def test_get_proverb_no_response():
    date_str='2024-12-25'
    date=datetime.strptime(date_str, '%Y-%m-%d')
    day = date.day
    month = date.month
    mock_html = '''<div class="calCard_proverb-content"></div>'''
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = mock_html.encode('utf-8')
        result = get_proverb(day, month)
        assert result == ['Brak przysłów']
        mock_get.assert_called_once_with("https://www.kalbi.pl/25-12")

def test_get_agh_news_successful_response():
    date_str="2024-12-25"
    date=datetime.strptime(date_str, '%Y-%m-%d')
    mock_html ='''<article class="d-md-flex">
                <span class="date">25.12.2024</span>
                <h2>Tytuł artykułu</h2>
                <p>Opis artykułu</p>
                <a href="/aktualnosci/1234">Czytaj więcej</a>
            </article>'''
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = mock_html.encode('utf-8')
        result = get_agh_news(date)
        assert result == {
            'title': 'Tytuł artykułu',
            'description': 'Opis artykułu',
            'link': None
        }
        mock_get.assert_called_once_with("https://www.agh.edu.pl/aktualnosci")

def test_get_agh_news_no_response():
    date_str="2024-12-25"
    date=datetime.strptime(date_str, '%Y-%m-%d')
    mock_html = '<html></html>'
    with patch('requests.get') as mock_get:
        mock_get.return_value.content = mock_html
        result = get_agh_news(date)
        assert result is None
        mock_get.assert_called_once_with("https://www.agh.edu.pl/aktualnosci")

def test_parse_date_standard():
    date_str = "2024-12-12"
    date, prev_date, next_date = parse_date(date_str)
    assert date.strftime('%Y-%m-%d') == "2024-12-12"
    assert prev_date == "2024-12-11"
    assert next_date == "2024-12-13"

def test_parse_date_end_of_year():
    date_str = "2024-12-31"
    date, prev_date, next_date = parse_date(date_str)
    assert date.strftime('%Y-%m-%d') == "2024-12-31"
    assert prev_date == "2024-12-30"
    assert next_date == "2025-01-01"

def test_parse_date_invalid_format():
    date_str = "12-12-2024"
    with pytest.raises(ValueError):
        parse_date(date_str)
    


def test_news_preview(client):
    response = client.get('/calendar/calendar_preview')
    assert response.status_code == 200