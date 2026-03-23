"""
Exercice 4: Validation de Formulaire

Usage:
    python exercice4.py

Testing:
    # Valid registration
    curl -X POST http://localhost:5000/register \
      -H "Content-Type: application/json" \
      -d '{"username": "john", "email": "john@example.com", "password": "secure123", "age": 25}'

    # All fields invalid
    curl -X POST http://localhost:5000/register \
      -H "Content-Type: application/json" \
      -d '{"username": "j", "email": "invalid", "password": "short", "age": 15}'
"""

from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# In-memory user database
users_db = {
    1: {
        "id": 1,
        "username": "john",
        "email": "john@example.com",
        "password": "secure123",
        "age": 25,
    }
}

next_user_id = 2

# Validation patterns
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
USERNAME_PATTERN = r'^[a-zA-Z0-9_]{2,20}$'


# ============================================================================
# Validation Functions
# ============================================================================

def validate_username(username):
    """
    Validate username (alphanumeric + underscore, 2-20 chars)

    Returns:
        (bool, str): (is_valid, error_message)
    """
    if not username or not isinstance(username, str):
        return False, "username is required"

    if not re.match(USERNAME_PATTERN, username):
        return False, "username too short" if len(username) < 2 else "invalid username format"

    return True, None


def validate_email(email):
    """
    Validate email format

    Returns:
        (bool, str): (is_valid, error_message)
    """
    if not email or not isinstance(email, str):
        return False, "email is required"

    if not re.match(EMAIL_PATTERN, email.strip()):
        return False, "invalid email"

    return True, None


def validate_password(password):
    """
    Validate password (minimum 8 characters)

    Returns:
        (bool, str): (is_valid, error_message)
    """
    if not password or not isinstance(password, str):
        return False, "password is required"

    if len(password) < 8:
        return False, "password too short"

    return True, None


def validate_age(age):
    """
    Validate age (must be integer between 18 and 100)

    Returns:
        (bool, str): (is_valid, error_message)
    """
    if age is None:
        return True, None  # age is optional

    try:
        age_int = int(age)
    except (ValueError, TypeError):
        return False, "age must be an integer"

    if age_int < 18:
        return False, "age must be 18+"

    if age_int > 100:
        return False, "age cannot exceed 100"

    return True, None


# ============================================================================
# Endpoints
# ============================================================================

@app.route('/register', methods=['POST'])
def register():
    """
    POST /register
    Register new user with validation, returns all errors at once

    Required fields:
        - username: 2-20 chars, alphanumeric + underscore
        - email: valid email format
        - password: minimum 8 characters

    Optional fields:
        - age: integer between 18 and 100

    Returns:
        201: User registered successfully
        400: Validation errors list
    """
    global next_user_id

    if not request.is_json:
        return jsonify({"errors": ["Content-Type must be application/json"]}), 400

    data = request.get_json()
    errors = []

    # Validate each field and collect all errors
    is_valid, error = validate_username(data.get('username', ''))
    if not is_valid:
        errors.append(error)

    is_valid, error = validate_email(data.get('email', ''))
    if not is_valid:
        errors.append(error)

    is_valid, error = validate_password(data.get('password', ''))
    if not is_valid:
        errors.append(error)

    is_valid, error = validate_age(data.get('age'))
    if not is_valid:
        errors.append(error)

    if errors:
        return jsonify({"errors": errors}), 400

    # All validations passed - create user
    new_user = {
        "id": next_user_id,
        "username": data['username'],
        "email": data['email'],
        "password": data['password'],
        "age": data.get('age')
    }

    users_db[next_user_id] = new_user
    next_user_id += 1

    return jsonify({"message": "Registration successful", "user": new_user}), 201


if __name__ == '__main__':
    app.run(debug=True, port=5000)