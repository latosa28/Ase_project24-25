import logging
from flask import Blueprint, jsonify, request

from errors.errors import HTTPNotFoundError, HTTPInternalServerError
from utils_helpers.token import token_required, admin_token_authorized
from models.models import User, db

admin_api = Blueprint('admin_api', __name__)


@admin_api.route('/users', methods=['GET'])
@token_required
def get_all_users():
    all_users = User.query.all()
    return jsonify([
        {"user_id": user.user_id, "username": user.username, "email": user.email} 
        for user in all_users
    ]), 200


@admin_api.route('/admin/<int:admin_id>/user/<int:user_id>', methods=['POST'])
@admin_token_authorized
def modify_user(admin_id, user_id):
    email = request.json.get('email')
    user = User.query.get(user_id)

    if not user:
        raise HTTPNotFoundError("User not found")

    try:
        user.email = email
        db.session.commit()
        return jsonify({}), 200
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while updating user: {str(e)}")
        raise HTTPInternalServerError()

