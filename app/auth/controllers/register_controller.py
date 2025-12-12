"""
Controller for handling user registration requests.
"""

from flask import Blueprint, request, jsonify
from app.auth.services.register_service import RegisterService
from app.utils.exceptions import BadRequestError

register_controller = Blueprint('register_controller', __name__)

@register_controller.route('/register', methods=['POST'])
def register_user():
    """Endpoint to register a new user."""
    try:
        data = request.json
        if not data:
            raise BadRequestError("Request body is missing.")
        
        email = data.get("email")
        password = data.get("password")
        RegisterService.register(email=email, password=password)
        return jsonify({"message": "User registered successfully. Confirmation email sent."}), 201
    except BadRequestError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred during registration."}), 500
