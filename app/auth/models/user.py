from typing import Optional
from app.database.models.base_model import BaseModel

class User(BaseModel):
    """Represents a user entity."""
    def __init__(self, username: str, password: str, session_data: Optional[dict] = None):
        self.username = username
        self.password = password
        self.session_data = session_data

    @staticmethod
    def find_by_username(username: str) -> Optional['User']:
        """Retrieves a user object by username."""
        # Replace with actual DB query implementation
        database_users = {
            "user1": User("user1", "hashed_password1", {"dashboard_url": "/dashboard"}),
            "user2": User("user2", "hashed_password2", {"dashboard_url": "/dashboard"})
        }
        return database_users.get(username)
