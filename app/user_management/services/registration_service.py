import logging
from typing import Optional
from app.database.models.user import User
from app.utils.email import send_confirmation_email
from app.utils.exceptions import ServiceError
from app.utils.validators import validate_email, validate_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RegistrationService:
    """
    Provides functionality to register a new user account.
    """

    @staticmethod
    def register_user(email: str, password: str) -> Optional[User]:
        """
        Handles user registration process.
        
        Validates input, ensures email uniqueness, enforces password security,
        registers the user, and sends a confirmation email.

        Args:
            email (str): The user's email address (must be unique).
            password (str): The user's password (must meet complexity criteria).

        Raises:
            ServiceError: Raised if validation fails or email already exists.

        Returns:
            User: Created User object if registration succeeds; None otherwise.
        """
        try:
            # Validate email and password
            if not validate_email(email):
                raise ServiceError("Invalid email format.")
            
            if not validate_password(password):
                raise ServiceError("Password does not meet complexity requirements.")

            # Check for existing user
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                raise ServiceError("Email is already in use.")

            # Create and save new user
            new_user = User(email=email, password=password)  # Password should be securely hashed in User model.
            new_user.save()

            # Send confirmation email
            send_confirmation_email(email)
            
            logger.info(f"User registered successfully: {email}")
            return new_user
        except ServiceError as e:
            logger.error(f"Registration failed: {e}")
            raise
        except Exception as ex:
            logger.error(f"Unexpected error during registration: {ex}")
            raise ServiceError("An unexpected error occurred. Please try again.")
