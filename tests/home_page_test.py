import os
import sys
import pytest

# Dodanie katalogu wyżej do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importowanie aplikacji
from app import app_setup

@pytest.fixture
def client():
    app = app_setup.test_client()
    app.testing = True
    yield app

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200