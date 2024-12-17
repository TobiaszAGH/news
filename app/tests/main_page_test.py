import pytest
import requests_mock
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

def test_home_page(client):
    with original_app.test_request_context():
        response = client.get('/')
        assert response.status_code == 200

def test_404_page(client):
    with original_app.test_request_context():
        response = client.get('/nonexistent')
        assert response.status_code == 404