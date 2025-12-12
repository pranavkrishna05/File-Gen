import logging
from typing import Dict
from datetime import datetime
from app.auth.models.user_model import User
from app.auth.models.password_reset_model import PasswordReset

# Initialize logger
logger = logging.getLogger(__name__)

class PasswordResetError(Exception):
    """Custom exception for password reset-related errors."""
    pass

def request_password_reset(data: Dict[str, str]) -> str:
    """Handles the creation of a password reset request.

    Args:
        data (Dict[str, str]): Contains the user's email.

    Returns:
        str: Confirmation message that reset link was sent.

    Raises:
        PasswordResetError: If no user with the provided email exists.
    """
    try:
        email = data.get('email')

        # Validate email
        if not email or not isinstance(email, str):
            raise PasswordResetError("Invalid email format")

        user = User.query.filter_by(email=email).first()
        if not user:
            raise PasswordResetError("No account found for this email")

        # Generate password reset token and expiry
        reset_token = PasswordReset.generate_token()
        expiry_time = PasswordReset.generate_expiry_time()

        # Create PasswordReset record
        password_reset = PasswordReset(user_id=user.id, reset_token=reset_token, expiry_time=expiry_time)
        password_reset.save()

        logger.info("Password reset requested for user %s", user.email)

        # Simulate sending email (replace with actual email function in production)
        logger.info("Password reset link: /reset-password?token=%s", reset_token)

        return "Password reset link has been sent to your email"
    except Exception as e:
        logger.error("Error during password reset request: %s", e)
        raise PasswordResetError(str(e)) from e

def reset_password(data: Dict[str, str]) -> str:
    """Handles the password reset using the provided token.

    Args:
        data (Dict[str, str]): Contains the reset token and new password.

    Returns:
        str: Confirmation message for successful reset.

    Raises:
        PasswordResetError: If the token is invalid, expired, or password criteria not met.
    """
    try:
        reset_token = data.get('reset_token')
        new_password = data.get('new_password')

        # Validate password and token
        if not reset_token or not new_password:
            raise PasswordResetError("Invalid reset token or password")

        if len(new_password) < 8 or not any(char.isdigit() for char in new_password):
            raise PasswordResetError("Password must be at least 8 characters long and include a number")

        password_reset = PasswordReset.query.filter_by(reset_token=reset_token).first()

        if not password_reset or password_reset.used:
            raise PasswordResetError("Invalid or already-used reset token")

        if password_reset.expiry_time < datetime.utcnow():
            raise PasswordResetError("Reset token has expired")

        # Update user password
        user = User.query.get(password_reset.user_id)
        user.password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        user.save()

        # Mark reset token as used
        password_reset.used = True
        password_reset.save()

        logger.info("Password successfully updated for user %s", user.email)
        return "Your password has been updated successfully"
    except Exception as e:
        logger.error("Error during password reset: %s", e)
        raise PasswordResetError(str(e)) from e