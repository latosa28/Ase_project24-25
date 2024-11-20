from flask import Blueprint, jsonify, request

from models.models import User, db

admin_api = Blueprint('admin_api', __name__)


@admin_api.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    return jsonify([{"username": user.username, "email": user.email} for user in all_users]), 200


@admin_api.route('/admin/<int:admin_id>/user/<int:user_id>', methods=['POST'])
def modify_user(admin_id, user_id):
    email = request.json.get('email')
    user = User.query.get(user_id)

    try:
        user.email = email
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "An error occurred while processing your request."}), 400

    return jsonify({}), 200
