import pytest
from flask import Flask
from app.auth.controllers.login_controller import login_controller

def test_successful_login(client):
    """Tests the login endpoint for successful login."""
    response = client.post('/login', json={'username': 'user1', 'password': 'valid_password'})
    assert response.status_code == 200
    assert "Login successful" in response.json['message']

def test_failed_login(client):
    """Tests the login endpoint for failed login."""
    response = client.post('/login', json={'username': 'user1', 'password': 'invalid_password'})
    assert response.status_code == 401
    assert "Invalid credentials" in response.json['message']

def test_invalid_request_format(client):
    """Tests invalid request format scenario."""
    response = client.post('/login', json={'wrong_field': 'value'})
    assert response.status_code == 400
    assert "Invalid request format" in response.json['message']