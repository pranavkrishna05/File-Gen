from flask import Blueprint, request, jsonify
from flask_mail import Mail
from app.auth.services.register_service import RegisterService
from app.utils.errors import ValidationError, RegistrationError

register_bp = Blueprint('register', __name__, url_prefix='/auth/register')

# Instantiate necessary dependencies
mail = Mail()
register_service = RegisterService(mail)

@register_bp.route('', methods=['POST'])
def register():
    """
    Endpoint to register a new user.

    :return: JSON response
    """
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required."}), 400

        # Call registration service
        response = register_service.register_user(email, password)
        return jsonify(response), 201

    except ValidationError as e:
        return jsonify({"error": e.message}), 400

    except RegistrationError as e:
        return jsonify({"error": e.message}), 409

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500
