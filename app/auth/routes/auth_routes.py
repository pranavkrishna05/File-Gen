import logging
from flask import Blueprint, request, jsonify
from app.auth.services.register_service import register_user, RegistrationError

# Initialize logger
logger = logging.getLogger(__name__)

# Blueprint setup
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Route for user registration."""
    try:
        data = request.get_json()
        message = register_user(data)
        return jsonify({"status": "success", "message": message}), 201
    except RegistrationError as e:
        logger.error("Registration failed: %s", e)
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        logger.error("Unexpected error during registration: %s", e)
        return jsonify({"status": "error", "message": "Internal server error."}), 500