import logging
from flask import Blueprint, request, jsonify
from app.auth.services.login_service import LoginService

logger = logging.getLogger(__name__)
login_controller = Blueprint('login_controller', __name__)

@login_controller.route('/login', methods=['POST'])
def login():
    """Handles user login requests."""
    try:
        data = request.json
        username = data['username']
        password = data['password']
        
        service = LoginService()
        result = service.authenticate_user(username, password)
        if result['status'] == 'success':
            return jsonify({"message": "Login successful", "data": result['data']}), 200
        else:
            return jsonify({"message": result['error']}), 401
    except KeyError:
        logger.error("Invalid request format")
        return jsonify({"message": "Invalid request format"}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500
