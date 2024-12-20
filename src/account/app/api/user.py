import logging

from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

from errors.errors import HTTPBadRequestError, HTTPError, HTTPInternalServerError, HTTPNotFoundError, HTTPForbiddenError
from helpers.currency import CurrencyHelper
from models.models import User, db
from utils_helpers.credentials import check_credentials
from utils_helpers.token import token_authorized
from utils_helpers.validation import email_validation, get_body_field

user_api = Blueprint('user_api', __name__)


# Route to create a new user
@user_api.route('/user', methods=['POST'])
def create_user():
    username = get_body_field('username')
    email = get_body_field('email')
    password = get_body_field('password')

    if not username or not email or not password:
        raise HTTPBadRequestError("Missing Data")

    email_validation(email)

    user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
    if user:
        raise HTTPBadRequestError("Invalid Credentials")

    password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, email=email, password=password)

    try:
        db.session.add(new_user)
        db.session.commit()
        response = CurrencyHelper().add_amount(new_user.user_id, 500)
        if response.status_code == 200:
            return jsonify({"user_id": new_user.user_id}), 201
        else:
            db.session.rollback()
            data = response.json()
            raise HTTPError(response.status_code, data.get('error'), data.get('error_description'))
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while creating user: {str(e)}")
        raise HTTPInternalServerError()


# Route to delete an existing user by ID
@user_api.route('/user/<int:user_id>', methods=['DELETE'])
@token_authorized
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({}), 200
        except Exception as e:
            db.session.rollback()
            raise HTTPInternalServerError()
    else:
        raise HTTPNotFoundError("User not found")


# Route to change info (email and/or password) to an existing user by ID
@user_api.route('/user/<int:user_id>', methods=['POST'])
@token_authorized
def change_user_info(user_id):
    email = get_body_field('email')
    password = get_body_field('password')

    if not password and not email:
        raise HTTPBadRequestError("Missing data to change")

    user = User.query.filter(User.user_id == user_id).first()

    if not user:
        raise HTTPNotFoundError("User not found")

    if email:
        email_validation(email)
        user.email = email

    if password:
        password = generate_password_hash(password, method='pbkdf2:sha256')
        user.password = password

    try:
        db.session.commit()
        return jsonify({"message": "User info update successfully"}), 200
    except Exception:
        db.session.rollback()
        raise HTTPInternalServerError()


# Route to get user details by ID
@user_api.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.serialize()), 200
    else:
        raise HTTPNotFoundError("User not found")


# Route to check account credentials
@user_api.route('/user/username/<string:username>/check_credentials', methods=['POST'])
def check_account_credentials(username):
    password = request.get_json()["password"]
    user = User.query.filter_by(username=username).first()
    if user:
        if check_credentials("user", username, user.password, password):
            return jsonify({"user_id": user.user_id}), 200
        raise HTTPForbiddenError("Invalid Credentials")
    else:
        raise HTTPNotFoundError("User not found")



