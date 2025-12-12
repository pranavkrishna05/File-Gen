import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize the database object
db = SQLAlchemy()

class Session(db.Model):
    """Session model to represent active user sessions."""
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        return f"<Session user_id={self.user_id}, login_time={self.login_time}>"

    def save(self) -> None:
        """Save the session record to the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            logger.error("Error saving session: %s", error)
            raise error