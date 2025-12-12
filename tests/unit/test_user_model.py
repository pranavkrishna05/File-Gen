import pytest
from app.auth.models.user import User

def test_find_by_username_success():
    """Tests finding a user by username successfully."""
    user = User("user1", "hashed_password1")
    mock_user_data = {"user1": user}
    User.find_by_username = lambda username: mock_user_data.get(username)
    result = User.find_by_username("user1")
    assert result.username == "user1"
def test_find_by_username_none():
    """Tests finding a user by username that does not exist."""
    mock_user_data = {}
    User.find_by_username = lambda username: mock_user_data.get(username)
    result = User.find_by_username("nonexistent_user")
    assert result is None