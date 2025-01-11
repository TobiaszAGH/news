from app import app as original_app

def test_home_page(client):
    with original_app.test_request_context():
        response = client.get('/')
        assert response.status_code == 200
        
def test_weather_page(client):
    with original_app.test_request_context():
        response = client.get('/weather/')
        assert response.status_code == 200

def test_economy_page(client):
    with original_app.test_request_context():
        response = client.get('/economy/')
        assert response.status_code == 200

def test_news_page(client):
    with original_app.test_request_context():
        response = client.get('/news/')
        assert response.status_code == 200

def test_sport_page(client):
    with original_app.test_request_context():
        response = client.get('/sport/')
        assert response.status_code == 200

def test_404_page(client):
    with original_app.test_request_context():
        response = client.get('/nonexistent')
        assert response.status_code == 404