import logging
from flask import Blueprint, jsonify, request

from errors.errors import HTTPNotFoundError, HTTPInternalServerError, HTTPBadRequestError
from utils_helpers.token import token_required, admin_token_authorized
from models.models import User, db

admin_api = Blueprint('admin_api', __name__)


@admin_api.route('/admin/<int:admin_id>/users', methods=['GET'])
@admin_token_authorized
def get_all_users(admin_id):
    all_users = User.query.all()
    return jsonify([
        user.serialize()
        for user in all_users
    ]), 200


@admin_api.route('/admin/<int:admin_id>/user/<int:user_id>', methods=['GET'])
@admin_token_authorized
def get_user_by_id(admin_id, user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.serialize()), 200
    else:
        raise HTTPNotFoundError("User not found")


@admin_api.route('/admin/<int:admin_id>/user/<int:user_id>', methods=['POST'])
@admin_token_authorized
def modify_user(admin_id, user_id):
    email = request.json.get('email')
    user = User.query.get(user_id)

    if not email:
        raise HTTPBadRequestError("Missing data to change")

    if not user:
        raise HTTPNotFoundError("User not found")

    user.email = email

    try:
        db.session.commit()
        return jsonify({"message": "User info update successfully"}), 200
    except Exception:
        db.session.rollback()
        raise HTTPInternalServerError()

