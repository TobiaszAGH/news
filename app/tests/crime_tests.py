import pytest
from datetime import date
from blueprints.news.models import CrimeNews, CrimeImage
from config import db

""" Tests """
# Models tests
def test_database_connection(crime_client):
    with crime_client.application.app_context():
        assert db.session.query(CrimeNews).count() == 0
        assert db.session.query(CrimeImage).count() == 0

def test_sample_news(crime_client, sample_news):
    with crime_client.application.app_context():
        assert db.session.query(CrimeNews).count() == 2
        assert db.session.query(CrimeImage).count() == 0

def test_sample_images(crime_client, sample_images):
    with crime_client.application.app_context():
        assert db.session.query(CrimeNews).count() == 0
        assert db.session.query(CrimeImage).count() == 3

def test_sample_data(crime_client, sample_data):
    with crime_client.application.app_context():
        assert db.session.query(CrimeNews).first().title == "News_1"
        assert db.session.query(CrimeImage).first().id == 1


# Routes tests
def test_news_home(crime_client, sample_data):
    response = crime_client.get('/news/')
    assert response.status_code == 200
    assert b"dla Krakowa" in response.data
    assert b"Summary_1" in response.data

def test_news_article(crime_client, sample_data):
    response = crime_client.get('/news/2')
    assert response.status_code == 200
    assert b"Description_2" in response.data

def test_news_preview(crime_client):
    response = crime_client.get('/news/news_preview')
    assert response.status_code == 200

def test_article_not_found(crime_client):
    response = crime_client.get('/news/999')
    assert b"nie istnieje" in response.data


# Scraping tests
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

    assert result['title'] == "Test Title"
    assert result['summary'] == "Test summary"
    assert result['image_src'] == "https://krakow.policja.gov.pl/test.jpg"
    assert result['date'].strftime("%d.%m.%Y") == "01.01.2023"



def test_fetch_article_description(requests_mock):
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

    assert description == "Description text"
    assert isinstance(soup, BeautifulSoup)

def test_save_article(crime_client):
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

        assert saved_article is not None
        assert saved_article.summary == 'Test Summary'
        assert saved_article.description == 'Test Description'
        assert saved_article.image_url == 'http://example.com/image.jpg'
        assert saved_article.article_link == full_link
        assert saved_article.publication_date == date(2023, 1, 1)


def test_save_images(crime_client):
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
        assert len(images) == 2
        assert images[0].image_url == 'https://krakow.policja.gov.pl/image1.jpg'
        assert images[1].image_url == 'https://krakow.policja.gov.pl/image2.jpg'
