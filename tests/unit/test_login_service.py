import pytest
from app.auth.services.login_service import LoginService

def test_authenticate_user_success(mocker):
    """Tests user authentication with valid credentials."""
    mocker.patch('app.auth.models.user.User.find_by_username', return_value=mocker.Mock(password='hashed_password'))
    service = LoginService()
    result = service.authenticate_user('valid_user', 'correct_password')
    assert result['status'] == 'success'
def test_authenticate_user_failed(mocker):
    """Tests user authentication with invalid credentials."""
    mocker.patch('app.auth.models.user.User.find_by_username', return_value=None)
    service = LoginService()
    result = service.authenticate_user('invalid_user', 'wrong_password')
    assert result['status'] == 'fail'
def test_service_error(mocker):
    """Tests user authentication when an exception occurs."""
    mocker.patch('app.auth.models.user.User.find_by_username', side_effect=Exception("DB Error"))
    service = LoginService()
    result = service.authenticate_user('any_user', 'any_password')
    assert result['status'] == 'error'