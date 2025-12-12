import logging
from flask import Blueprint, request, jsonify
from app.auth.services.password_reset_service import request_password_reset, reset_password, PasswordResetError

# Initialize logger
logger = logging.getLogger(__name__)

# Blueprint setup
password_reset_bp = Blueprint('password_reset', __name__, url_prefix='/auth')

@password_reset_bp.route('/request-reset', methods=['POST'])
def request_reset():
    """Route for requesting password reset."""
    try:
        data = request.get_json()
        message = request_password_reset(data)
        return jsonify({"status": "success", "message": message}), 200
    except PasswordResetError as e:
        logger.error("Password reset request failed: %s", e)
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        logger.error("Unexpected error during password reset request: %s", e)
        return jsonify({"status": "error", "message": "Internal server error."}), 500

@password_reset_bp.route('/reset-password', methods=['POST'])
def reset():
    """Route for resetting password using reset token."""
    try:
        data = request.get_json()
        message = reset_password(data)
        return jsonify({"status": "success", "message": message}), 200
    except PasswordResetError as e:
        logger.error("Password reset failed: %s", e)
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        logger.error("Unexpected error during password reset: %s", e)
        return jsonify({"status": "error", "message": "Internal server error."}), 500