"""
Unit tests for RegisterService.
"""

import pytest
from app.auth.services.register_service import RegisterService
from app.database.models.user import User
from app.utils.exceptions import BadRequestError

@pytest.fixture
def mock_user_model(mocker):
    return mocker.patch('app.database.models.user.User')

def test_register_success(mock_user_model, mocker):
    """Test successful user registration."""
    mock_user_model.query.filter_by.return_value.first.return_value = None
    mocker.patch('app.auth.services.register_service.RegisterService.hash_password', return_value='hashed_password')
    mocker.patch('app.utils.email_utils.send_confirmation_email', return_value=None)

    RegisterService.register(email="test@example.com", password="Password123")
    mock_user_model.assert_called()

def test_register_existing_email(mock_user_model):
    """Test registration with an existing email."""
    mock_user_model.query.filter_by.return_value.first.return_value = User(email="test@example.com")

    with pytest.raises(BadRequestError, match="Email is already registered."):
        RegisterService.register(email="test@example.com", password="Password123")

def test_register_invalid_email():
    """Test registration with invalid email format."""
    with pytest.raises(BadRequestError, match="Invalid email format."):
        RegisterService.register(email="invalid-email", password="Password123")

def test_register_insecure_password():
    """Test registration with insecure password."""
    with pytest.raises(BadRequestError, match="Password does not meet security requirements."):
        RegisterService.register(email="test@example.com", password="short")
