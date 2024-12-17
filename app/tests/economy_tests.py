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
