import logging
from typing import Optional
from flask_sqlalchemy import SQLAlchemy

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize the database object
db = SQLAlchemy()

class User(db.Model):
    """User model representing a registered user."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_confirmed = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def save(self) -> None:
        """Save the user record to the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            logger.error("Error saving user: %s", error)
            raise error