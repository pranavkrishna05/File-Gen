import logging
from typing import Optional
from werkzeug.security import generate_password_hash
from app.user_management.models.user import db, User

logger = logging.getLogger(__name__)

class UserService:
    """Service layer for operations related to user accounts."""

    @staticmethod
    def register_user(email: str, password: str) -> Optional[User]:
        """
        Registers a new user with the given email and password.
        
        :param email: User's email address
        :param password: User's password
        :return: The newly created User object, or None if registration fails
        """
        if User.query.filter_by(email=email).first():
            logger.warning(f"Registration failed: Email {email} already exists.")
            return None

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password_hash=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"User {email} registered successfully.")
            return new_user
        except Exception as e:
            logger.error(f"Error occurred while registering user {email}: {str(e)}")
            db.session.rollback()
            return None