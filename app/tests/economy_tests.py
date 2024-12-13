from flask import Flask
from flask.testing import FlaskClient
import pytest
from blueprints.economy.routes import economy_bp



# Testowanie endpointu '/weather'
def test_economy_endpoint(client: FlaskClient):
    with client:
        response = client.get('/economy/')
        print(response.data) 
        assert response.status_code == 200

def test_start_after_end(client: FlaskClient):
    with client:
        response = client.post('/economy/', data={"startdate": "2024-11-11", "todate": "2024-10-10", "currency1": "USD"})
        assert response.status_code == 200
        assert bytes("Start musi być wcześniej niż koniec!", "utf-8") in response.data

def test_correct_economy(client: FlaskClient):
    with client:
        response = client.post('/economy/', data={"startdate": "2024-11-11", "todate": "2024-12-12", "currency1": "USD"})
        assert response.status_code == 200
        assert bytes("Kursy waluty w PLN", 'utf-8') in response.data