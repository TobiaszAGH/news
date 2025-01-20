from datetime import datetime
import requests
from blueprints.sport.models import SportArticle
from config import db 



# Test jednostkowy - Model
# Sprawdza, czy model 'SportArticle' poprawnie przechowuje dane, 
# takie jak tytuł, opis, link, czy typ sportu.

def test_sport_article_model():
    article = SportArticle(
        title="Test Article",
        description="Test Description",
        image_url="http://example.com/image.jpg",
        pubDate=datetime(2025, 1, 1),
        link="http://example.com/article",
        sport_type="football",
    )
    assert article.title == "Test Article"
    assert article.description == "Test Description"
    assert article.image_url == "http://example.com/image.jpg"
    assert article.pubDate == datetime(2025, 1, 1)
    assert article.link == "http://example.com/article"
    assert article.sport_type == "football"



# Test jednostkowy - Połączenie z zewnętrznym API
# Symuluje odpowiedź z zewnętrznego API i sprawdza, 
# czy aplikacja poprawnie pobiera dane.

def test_sport_api_fetch(requests_mock):
    api_url = "https://newsdata.io/api/1/news"
    sport_data = {
        "results": [
            {
                "title": "API Article",
                "description": "API Description",
                "image_url": "http://example.com/api.jpg",
                "pubDate": "2025-01-15 10:00:00",
                "link": "http://example.com/api-article",
            }
        ]
    }
    requests_mock.get(api_url, json=sport_data)

    response = requests.get(api_url)
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["title"] == "API Article"


# Test jednostkowy
# Symuluje błąd serwera API (kod 500) i sprawdza, 
# czy aplikacja poprawnie reaguje na błędne odpowiedzi.

def test_sport_api_fetch_error(requests_mock):
    api_url = "https://newsdata.io/api/1/news"
    requests_mock.get(api_url, status_code=500)

    response = requests.get(api_url)
    assert response.status_code == 500



# Test integracyjny - Endpoint sport_home
# Sprawdza, czy endpoint '/sport/' poprawnie zwraca artykuły, 
# które znajdują się w bazie danych.

def test_sport_home_with_articles(db_client):
    with db_client.application.app_context():
        article = SportArticle(
            title="Test Article",
            description="Test Description",
            image_url="http://example.com/image.jpg",
            pubDate=datetime(2025, 1, 1),
            link="http://example.com/article",
            sport_type="football",
        )
        db.session.add(article)
        db.session.commit()

    response = db_client.get('/sport/')
    assert response.status_code == 200
    assert b"Test Article" in response.data
    assert b"Test Description" in response.data



# Test integracyjny
# Sprawdza, czy endpoint '/sport/' poprawnie obsługuje artykuły 
# bez zdjęcia (pole 'image_url' jest 'None').


def test_sport_home_article_no_image(db_client):
    with db_client.application.app_context():
        article = SportArticle(
            title="Test Article Without Image",
            description="Description Without Image",
            image_url=None,
            pubDate=datetime(2025, 1, 1),
            link="http://example.com/article",
            sport_type="football",
        )
        db.session.add(article)
        db.session.commit()

    response = db_client.get('/sport/')
    assert response.status_code == 200
    assert b"Test Article Without Image" in response.data
    assert "Brak zdjęcia".encode('utf-8') in response.data


# Test integracyjny - Filtr dyscyplin
# Sprawdza, czy filtrowanie artykułów po dyscyplinie sportu 
# ('football', 'tennis') działa poprawnie.

def test_sport_home_filter_discipline(db_client):
    with db_client.application.app_context():
        article1 = SportArticle(
            title="Football Article",
            description="Football Description",
            image_url="http://example.com/football.jpg",
            pubDate=datetime(2025, 1, 1),
            link="http://example.com/football",
            sport_type="football",
        )
        article2 = SportArticle(
            title="Tennis Article",
            description="Tennis Description",
            image_url="http://example.com/tennis.jpg",
            pubDate=datetime(2025, 1, 2),
            link="http://example.com/tennis",
            sport_type="tennis",
        )
        db.session.add_all([article1, article2])
        db.session.commit()

    response = db_client.get('/sport/?discipline=tennis')
    assert response.status_code == 200
    assert b"Tennis Article" in response.data
    assert b"Football Article" not in response.data



# Test integracyjny
# Sprawdza, czy aplikacja poprawnie obsługuje przypadek, 
# gdy nie ma artykułów dla wybranej dyscypliny.


def test_sport_home_filter_no_results(db_client):
    with db_client.application.app_context():
        article = SportArticle(
            title="Football Article",
            description="Football Description",
            image_url="http://example.com/football.jpg",
            pubDate=datetime(2025, 1, 1),
            link="http://example.com/football",
            sport_type="football",
        )
        db.session.add(article)
        db.session.commit()

    response = db_client.get('/sport/?discipline=tennis')
    assert response.status_code == 200
    assert b"Football Article" not in response.data


# Test integracyjny - sport_preview endpoint
# Sprawdza, czy endpoint '/sport/sport_preview' poprawnie wyświetla 
# najnowszy artykuł.

def test_sport_preview(db_client):
    with db_client.application.app_context():
        article = SportArticle(
            title="Ski Jumping Article",
            description="Ski Jumping Description",
            image_url="http://example.com/ski.jpg",
            pubDate=datetime(2025, 1, 3),
            link="http://example.com/ski",
            sport_type="ski_jumping",
        )
        db.session.add(article)
        db.session.commit()

    response = db_client.get('/sport/sport_preview')
    assert response.status_code == 200
    assert b"Ski Jumping Article" in response.data
