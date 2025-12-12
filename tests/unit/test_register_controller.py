"""
Unit tests for RegisterController.
"""

import pytest
from flask import Flask
from app.auth.controllers.register_controller import register_controller

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(register_controller, url_prefix='/auth')
    app.testing = True
    return app.test_client()

def test_register_user_success(client, mocker):
    """Test successful user registration."""
    mock_service = mocker.patch('app.auth.services.register_service.RegisterService.register')
    mock_service.return_value = None

    response = client.post('/auth/register', json={"email": "test@example.com", "password": "Password123"})

    assert response.status_code == 201
    assert response.json == {"message": "User registered successfully. Confirmation email sent."}

def test_register_user_bad_request(client):
    """Test registering user with missing data."""
    response = client.post('/auth/register', json={})

    assert response.status_code == 400
    assert "Request body is missing." in response.json['error']

def test_register_user_server_error(client, mocker):
    """Test server error during registration."""
    mock_service = mocker.patch('app.auth.services.register_service.RegisterService.register')
    mock_service.side_effect = Exception("Unexpected Error")

    response = client.post('/auth/register', json={"email": "test@example.com", "password": "Password123"})

    assert response.status_code == 500
    assert "An error occurred during registration." in response.json['error']
