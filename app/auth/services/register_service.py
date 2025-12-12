"""
Service class to handle business logic for user registration.
"""

import logging
from app.database.models.user import User
from app.utils.email_utils import send_confirmation_email
from app.utils.exceptions import BadRequestError

logger = logging.getLogger(__name__)

class RegisterService:
    """Handles user registration-related business logic."""

    @staticmethod
    def register(email: str, password: str) -> None:
        """
        Registers a new user.

        Args:
            email (str): User's email.
            password (str): Plain text password.

        Raises:
            BadRequestError: If the user email already exists or password is invalid.
            ValueError: If email or password is missing.
        """
        if not email or not password:
            raise ValueError("Email and password are required.")

        if not RegisterService.is_email_valid(email):
            raise BadRequestError("Invalid email format.")

        if not RegisterService.is_password_secure(password):
            raise BadRequestError("Password does not meet security requirements.")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise BadRequestError("Email is already registered.")

        new_user = User(email=email, password=RegisterService.hash_password(password))
        new_user.save()

        send_confirmation_email(new_user.email)
        logger.info(f"User registered successfully: {email}")

    @staticmethod
    def is_email_valid(email: str) -> bool:
        """Validates email format."""
        import re
        email_regex = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def is_password_secure(password: str) -> bool:
        """Ensures password meets security criteria."""
        return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes the user's password."""
        from werkzeug.security import generate_password_hash
        return generate_password_hash(password)
