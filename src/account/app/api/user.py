import logging

from flask import Blueprint, jsonify, request

from errors.errors import HTTPBadRequestError, HTTPError, HTTPInternalServerError, HTTPNotFoundError
from helpers.currency import CurrencyHelper
from models.models import User, db
from utils_helpers.token import token_required, token_authorized

user_api = Blueprint('user_api', __name__)


# Route to create a new user
@user_api.route('/user', methods=['POST'])
def create_user():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    if not username or not email or not password:
        raise HTTPBadRequestError("Missing Data")

    user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
    if user:
        raise HTTPBadRequestError("Invalid Credentials")

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


# Route to get user details by ID
@user_api.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"name": user.username, "email": user.email}), 200
    else:
        raise HTTPNotFoundError("User not found")


# Route to get user details by username
@user_api.route('/user/username/<string:username>', methods=['GET'])
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(user.serialize()), 200
    else:
        raise HTTPNotFoundError("User not found")


