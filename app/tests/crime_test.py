import pytest
from config import db
from flask import Flask
from blueprints.news.routes import news_bp
from blueprints.main.routes import main_bp 
from config import Config

@pytest.fixture
def app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(Config)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(news_bp, url_prefix='/news', template_folder='templates')
    app.register_blueprint(main_bp, url_prefix='/') 

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
        
@pytest.fixture
def crime_client(app):
    return app.test_client()

from blueprints.news.models import CrimeNews, CrimeImage

@pytest.fixture
def sample_data(app):
    with app.app_context():
        news1 = CrimeNews(
            id=1, 
            title="News_1", 
            summary="Summary_1",
            description="Description_1",
            article_link="http://article_link_1.com",
            publication_date="2024-12-06"
            )
        
        news2 = CrimeNews(
            id=2, 
            title="News_2", 
            summary="Summary_2",
            description="Description_2",
            article_link="http://article_link_2.com",
            publication_date="2024-12-07"
            )
        db.session.add_all([news1, news2])
        db.session.commit()


def test_news_home(crime_client):
    response = crime_client.get('/news/')
    assert response.status_code == 200
    
    
def test_single_news(client):
    response = client.get('/news/1')
    assert response.status_code == 200
    assert b"News_1" in response.data
    assert b"Description_1" in response.data

    response = client.get('/news/999')
    assert response.status_code == 404

