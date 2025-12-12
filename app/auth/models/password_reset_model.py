import logging
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
import uuid

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize the database object
db = SQLAlchemy()

class PasswordReset(db.Model):
    """Model for managing user password reset requests."""
    __tablename__ = 'password_resets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    reset_token = db.Column(db.String(128), unique=True, nullable=False)
    expiry_time = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"<PasswordReset user_id={self.user_id}, token={self.reset_token}>"

    @staticmethod
    def generate_token() -> str:
        """Generates a unique token for password reset."""
        return str(uuid.uuid4())

    @staticmethod
    def generate_expiry_time(hours: int = 24) -> datetime:
        """Generates expiry time for the token."""
        return datetime.utcnow() + timedelta(hours=hours)

    def save(self) -> None:
        """Save the password reset record to the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            logger.error("Error saving password reset record: %s", error)
            raise error