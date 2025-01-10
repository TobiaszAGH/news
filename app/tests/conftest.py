import pytest
import requests_mock
from datetime import date
from flask import Flask
from flask.testing import FlaskClient
from app import app as original_app
from config import db
from blueprints.news.models import CrimeNews, CrimeImage
from blueprints.economy.economyData import economyData

@pytest.fixture
def client():
    app = original_app
    app.config['TESTING'] = True
    return app.test_client()


@pytest.fixture
def mocked_responses():
    with requests_mock.Mocker() as m:
        yield m

""" Economy fixtures """
@pytest.fixture
def economy_data():
    economy_data = economyData()
    return economy_data

""" News fixtures """
@pytest.fixture
def crime_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from blueprints.main.routes import main_bp
    from blueprints.news.routes import news_bp
    from blueprints.sport.routes import sport_bp
    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(news_bp, url_prefix='/news')
    app.register_blueprint(sport_bp, url_prefix='/sport')

    return app

@pytest.fixture
def test_db(crime_app):
    with crime_app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture
def crime_client(crime_app, test_db):
    with crime_app.app_context():
        return crime_app.test_client()

@pytest.fixture
def sample_news(crime_client):
    with crime_client.application.app_context():
        news1 = CrimeNews(
            id=1,
            title="News_1",
            summary="Summary_1",
            description="Description_1",
            article_link="http://article_link_1.com",
            publication_date=date(2024, 12, 6)
        )

        news2 = CrimeNews(
            id=2,
            title="News_2",
            summary="Summary_2",
            description="Description_2",
            article_link="http://article_link_2.com",
            publication_date=date(2024, 12, 7)
        )
        db.session.add_all([news1, news2])
        db.session.commit()
    yield

    with crime_client.application.app_context():
        db.session.query(CrimeNews).delete()
        db.session.commit()

@pytest.fixture
def sample_images(crime_client):
    with crime_client.application.app_context():
        image1 = CrimeImage(
            image_url="http://image1.com",
            news_id=1
        )
        image2 = CrimeImage(
            image_url="http://image2.com",
            news_id=1
        )
        image3 = CrimeImage(
            image_url="http://image3.com",
            news_id=2
        )

        db.session.add_all([image1, image2, image3])
        db.session.commit()
    yield

    with crime_client.application.app_context():
        db.session.query(CrimeImage).delete()
        db.session.commit()

@pytest.fixture
def sample_data(sample_images, sample_news):
    yield
