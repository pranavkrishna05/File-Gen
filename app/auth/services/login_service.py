import logging
from typing import Dict, Any
from app.auth.models.user import User
from werkzeug.security import check_password_hash

logger = logging.getLogger(__name__)

class LoginService:
    """Handles user authentication logic."""
    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """Validates user credentials."""
        try:
            user = User.find_by_username(username)
            if user and check_password_hash(user.password, password):
                # Assuming user.session_data holds session info.
                return {"status": "success", "data": user.session_data}
            else:
                logger.warning(f"Authentication failed for user '{username}'")
                return {"status": "fail", "error": "Invalid credentials"}
        except Exception as e:
            logger.error(f"Error during authentication: {str(e)}")
            return {"status": "error", "error": "Server error"}
