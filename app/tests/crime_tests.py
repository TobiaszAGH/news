from datetime import date
from blueprints.news.models import CrimeNews, CrimeImage
from config import db

# Testy modeli
def test_database_connection(crime_client):
    # Testuje, czy połączenie z bazą danych działa poprawnie
    with crime_client.application.app_context():
        assert db.session.query(CrimeNews).count() == 0  # Sprawdza, czy tabela CrimeNews jest pusta
        assert db.session.query(CrimeImage).count() == 0  # Sprawdza, czy tabela CrimeImage jest pusta

def test_sample_news(crime_client, sample_news):
    # Testuje wstawienie przykładowych danych do tabeli CrimeNews
    with crime_client.application.app_context():
        assert db.session.query(CrimeNews).count() == 2  # Sprawdza, czy są 2 artykuły
        assert db.session.query(CrimeImage).count() == 0  # Sprawdza, czy nie ma obrazów

def test_sample_images(crime_client, sample_images):
    # Testuje wstawienie przykładowych danych do tabeli CrimeImage
    with crime_client.application.app_context():
        assert db.session.query(CrimeNews).count() == 0  # Sprawdza, czy nie ma artykułów
        assert db.session.query(CrimeImage).count() == 3  # Sprawdza, czy są 3 obrazy

def test_sample_data(crime_client, sample_data):
    # Testuje, czy przykładowe dane zostały poprawnie zapisane
    with crime_client.application.app_context():
        assert db.session.query(CrimeNews).first().title == "News_1"  # Sprawdza tytuł pierwszego artykułu
        assert db.session.query(CrimeImage).first().id == 1  # Sprawdza ID pierwszego obrazu


# Testy tras
def test_news_home(crime_client, sample_data):
    # Testuje, czy strona główna artykułów działa poprawnie
    response = crime_client.get('/news/')
    assert response.status_code == 200  # Sprawdza, czy kod odpowiedzi to 200
    assert b"dla Krakowa" in response.data  # Sprawdza, czy zawartość zawiera określony tekst
    assert b"Summary_1" in response.data  # Sprawdza, czy zawartość zawiera streszczenie artykułu

def test_news_article(crime_client, sample_data):
    # Testuje, czy strona szczegółów artykułu działa poprawnie
    response = crime_client.get('/news/2')
    assert response.status_code == 200  # Sprawdza, czy kod odpowiedzi to 200
    assert b"Description_2" in response.data  # Sprawdza, czy zawiera opis artykułu

def test_news_preview(crime_client):
    # Testuje, czy strona podglądu działa poprawnie
    response = crime_client.get('/news/news_preview')
    assert response.status_code == 200  # Sprawdza, czy kod odpowiedzi to 200

def test_article_not_found(crime_client):
    # Testuje, czy wyświetlany jest komunikat błędu dla nieistniejącego artykułu
    response = crime_client.get('/news/999')
    assert b"nie istnieje" in response.data  # Sprawdza, czy zawiera komunikat o błędzie


# Testy skrapowania danych
import requests_mock
from bs4 import BeautifulSoup
from blueprints.news.data_scraper import (
    fetch_article,
    fetch_article_description,
    save_article,
    save_images,
    scrape_and_save,
    base_url
)

def test_fetch_article():
    # Testuje funkcję pobierania artykułu z kodu HTML
    html = '''
    <div>
        <p>Test summary</p>
        <img src="/test.jpg"/>
        <span class="data">Dodano: 01.01.2023</span>
    </div>
    '''
    article = BeautifulSoup(html, 'html.parser')
    title = "Test Title"

    result = fetch_article(article, title)

    assert result['title'] == "Test Title"  # Sprawdza poprawność tytułu
    assert result['summary'] == "Test summary"  # Sprawdza poprawność streszczenia
    assert result['image_src'] == "https://krakow.policja.gov.pl/test.jpg"  # Sprawdza URL obrazu
    assert result['date'].strftime("%d.%m.%Y") == "01.01.2023"  # Sprawdza poprawność daty

def test_fetch_article_description(requests_mock):
    # Testuje funkcję pobierania opisu artykułu
    test_url = "http://test.com/article"
    requests_mock.get(test_url, text='''
        <html>
            <p>P1</p>
            <p>P2</p>
            <p>P3</p>
            <p>Description text</p>
            <p>P5</p>
        </html>
    ''')

    description, soup = fetch_article_description(test_url)

    assert description == "Description text"  # Sprawdza, czy opis jest poprawny
    assert isinstance(soup, BeautifulSoup)  # Sprawdza, czy wynik to obiekt BeautifulSoup

def test_save_article(crime_client):
    # Testuje funkcję zapisu artykułu do bazy danych
    with crime_client.application.app_context():
        article_data = {
            'title': 'Test Article',
            'summary': 'Test Summary',
            'image_src': 'http://example.com/image.jpg',
            'date': date(2023, 1, 1)
        }
        full_link = 'http://example.com/article'
        description = 'Test Description'

        save_article(article_data, full_link, description)

        saved_article = CrimeNews.query.filter_by(title='Test Article').first()

        assert saved_article is not None  # Sprawdza, czy artykuł został zapisany
        assert saved_article.summary == 'Test Summary'  # Sprawdza poprawność streszczenia
        assert saved_article.description == 'Test Description'  # Sprawdza poprawność opisu
        assert saved_article.image_url == 'http://example.com/image.jpg'  # Sprawdza URL obrazu
        assert saved_article.article_link == full_link  # Sprawdza link artykułu
        assert saved_article.publication_date == date(2023, 1, 1)  # Sprawdza datę publikacji

def test_save_images(crime_client):
    # Testuje funkcję zapisu obrazów powiązanych z artykułem
    with crime_client.application.app_context():
        news_obj = CrimeNews(
            title='Test Article',
            summary='Test Summary',
            description='Test Description',
            image_url='http://example.com/image.jpg',
            article_link='http://example.com/article',
            publication_date=date(2023, 1, 1)
        )
        db.session.add(news_obj)
        db.session.commit()

        html = '''
        <html>
            <img src="/image1.jpg"/>
            <img src="/image2.jpg"/>
        </html>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        save_images(soup, news_obj)

        images = CrimeImage.query.filter_by(news_id=news_obj.id).all()
        assert len(images) == 2  # Sprawdza, czy zapisano 2 obrazy
        assert images[0].image_url == 'https://krakow.policja.gov.pl/image1.jpg'  # Sprawdza pierwszy URL
        assert images[1].image_url == 'https://krakow.policja.gov.pl/image2.jpg'  # Sprawdza drugi URL
