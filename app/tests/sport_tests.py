import pytest
import requests_mock
from flask import url_for
from app import app as original_app


@pytest.fixture
def client():
    app = original_app
    app.config['TESTING'] = True
    with app.app_context():
        with app.test_client() as client:
            yield client


@pytest.fixture
def mocked_responses():
    with requests_mock.Mocker() as m:
        yield m


# Testy jednostkowe
def test_sport_home(client):
    """Testuje renderowanie strony głównej sekcji sportowej."""
    with original_app.test_request_context():  # Dodanie kontekstu żądania
        response = client.get(url_for('sport.sport_home'))
        assert response.status_code == 200
        assert b"Wybierz sport:" in response.data


def test_sport_articles_invalid_sport(client):
    """Testuje zachowanie dla nieznanego sportu."""
    with original_app.test_request_context():  
        response = client.get(url_for('sport.sport_articles', sport_type='unknown'))
        assert response.status_code == 200
        #assert b"Nie znaleziono zadanego zasobu." in response.data


# Testy z wykorzystaniem mock API
def test_sport_articles_football(client, mocked_responses):
    """Testuje poprawne pobranie artykułów dla piłki nożnej."""
    with original_app.test_request_context():
        api_url = "https://newsdata.io/api/1/news?apikey=pub_593496808acfb9d29e8410845a3b9602f5863&q=pi%C5%82ka%20no%C5%BCna&country=pl&category=sports"
        mocked_responses.get(api_url, json={
            "results": [
                {
                    "title": "Football news title",
                    "description": "Football news description",
                    "image_url": "http://example.com/image.jpg",
                    "pubDate": "2024-01-01",
                    "link": "http://example.com/article"
                }
            ]
        })

        response = client.get(url_for('sport.sport_articles', sport_type='football'))
        assert response.status_code == 200
        assert b"Football news title" in response.data
        assert b"Football news description" in response.data
        assert b"2024-01-01" in response.data


# Testy integracyjne
def test_sport_article_integration(client, mocked_responses):
    """Testuje integrację API z renderowaniem artykułów."""
    with original_app.test_request_context():
        api_url = "https://newsdata.io/api/1/news?apikey=pub_593496808acfb9d29e8410845a3b9602f5863&q=tenis&country=pl&category=sports"
        mocked_responses.get(api_url, json={
            "results": [
                {
                    "title": "Tennis news title",
                    "description": "Tennis news description",
                    "image_url": "http://example.com/image.jpg",
                    "pubDate": "2024-02-01",
                    "link": "http://example.com/article"
                }
            ]
        })

        response = client.get(url_for('sport.sport_articles', sport_type='tennis'))
        assert response.status_code == 200
        assert b"Tennis news title" in response.data
        assert b"Tennis news description" in response.data
        assert b"2024-02-01" in response.data


# Test błędów API
def test_sport_articles_api_error(client, mocked_responses):
    """Testuje obsługę błędu API."""
    with original_app.test_request_context():
        api_url = "https://newsdata.io/api/1/news?apikey=pub_593496808acfb9d29e8410845a3b9602f5863&q=skoki%20narciarskie&country=pl&category=sports"
        mocked_responses.get(api_url, status_code=500)
        response = client.get(url_for('sport.sport_articles', sport_type='ski_jumping'))
        assert response.status_code == 200
        #assert b"Nie udalo sie zaladowac artykulow." in response.data
