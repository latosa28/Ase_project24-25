import logging

from flask import Blueprint, jsonify, request

from helpers.currency import CurrencyHelper
from models.models import User, db

user_api = Blueprint('user_api', __name__)


# Route to create a new user
@user_api.route('/user', methods=['POST'])
def create_user():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    if not username or not email or not password:
        return jsonify({"message": "Missing data"}), 400

    user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "User with this username or email already exists"}), 400

    new_user = User(username=username, email=email, password=password)

    try:
        db.session.add(new_user)
        db.session.commit()
        response = CurrencyHelper().add_amount(new_user.user_id, 500)
        if response.status_code == 200:
            return jsonify({"user_id": new_user.user_id}), 201
        else:
            db.session.rollback()
            return jsonify({"message": response.json().get('error', 'An error occurred')}), response.status_code
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while creating user: {str(e)}")
        return jsonify({"message": "An error occurred while processing your request."}), 400


# Route to delete an existing user by ID
@user_api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        try:
            # Delete the user and commit the changes
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"}), 200
        except Exception as e:
            # In case of an error, rollback the transaction
            db.session.rollback()
            return jsonify({"message": str(e)}), 500
    else:
        # If the user is not found, return a 404 error
        return jsonify({"message": "User not found"}), 404


# Route to get user details by ID
@user_api.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"username": user.username, "email": user.email}), 200
    else:
        # If the user is not found, return a 404 error
        return jsonify({"message": "User not found"}), 404


# Route to get user details by username
@user_api.route('/user/username/<string:username>', methods=['GET'])
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(user.serialize()), 200
    else:
        return jsonify({"message": "User not found"}), 404


# Route to get all users
@user_api.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    return jsonify([{"username": user.username, "email": user.email} for user in all_users]), 200
