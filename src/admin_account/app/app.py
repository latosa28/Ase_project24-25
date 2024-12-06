import logging
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from errors.error_handler import register_errors
from errors.errors import HTTPBadRequestError, HTTPInternalServerError, HTTPNotFoundError, HTTPForbiddenError
from models.models import Admin, db
from utils_helpers.config import load_config
from utils_helpers.credentials import check_credentials
from utils_helpers.validation import email_validation, get_body_field

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


def setup():
    load_config(app)
    register_errors(app)
    db.init_app(app)


setup()


# Route to create a new admin
@app.route("/admin", methods=["POST"])
def create_admin():
    username = get_body_field("username")
    email = get_body_field("email")
    password = get_body_field("password")

    if not username or not email or not password:
        raise HTTPBadRequestError("Missing Data")

    email_validation(email)
    admin = (
        Admin.query.filter_by(username=username).first()
        or Admin.query.filter_by(email=email).first()
    )
    if admin:
        raise HTTPBadRequestError("Invalid Credentials")

    password = generate_password_hash(password, method='pbkdf2:sha256')
    new_admin = Admin(username=username, email=email, password=password)

    try:
        db.session.add(new_admin)
        db.session.commit()
        return jsonify({"admin_id": new_admin.admin_id}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while creating admin: {str(e)}")
        raise HTTPInternalServerError()


# Route to delete an existing user by ID
@app.route("/admin/<int:admin_id>", methods=["DELETE"])
def delete_admin(admin_id):
    admin = Admin.query.get(admin_id)
    if admin:
        try:
            db.session.delete(admin)
            db.session.commit()
            return jsonify({"message": "Admin deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            raise HTTPInternalServerError()
    else:
        raise HTTPNotFoundError("Admin not found")


# Route to get user details by ID
@app.route("/admin/<int:admin_id>", methods=["GET"])
def get_admin_by_id(admin_id):
    admin = Admin.query.get(admin_id)
    if admin:
        return jsonify(admin.serialize()), 200
    else:
        raise HTTPNotFoundError("Admin not found")


# Route to check account credentials
@app.route('/admin/username/<string:username>/check_credentials', methods=['POST'])
def check_account_credentials(username):
    password = request.get_json()["password"]
    admin = Admin.query.filter_by(username=username).first()
    if admin:
        if check_credentials("admin", username, admin.password, password):
            return jsonify({"admin_id": admin.admin_id}), 200
        return HTTPForbiddenError("Invalid Credentials")
    else:
        raise HTTPNotFoundError("Admin not found")


# Run the application
if __name__ == "__main__":
    # Set host to '0.0.0.0' to make the app accessible from other containers
    app.run(host='127.0.0.1', port=5010)
