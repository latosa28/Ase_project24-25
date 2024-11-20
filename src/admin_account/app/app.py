import logging
from flask import Flask, request, jsonify

from conf.config import load_config
from models.models import Admin, db

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


def setup():
    load_config(app)
    db.init_app(app)


setup()


# Route to create a new admin
@app.route("/admin", methods=["POST"])
def create_admin():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Missing data"}), 400

    admin = (
        Admin.query.filter_by(username=username).first()
        or Admin.query.filter_by(email=email).first()
    )
    if admin:
        return (
            jsonify({"message": "User with this username or email already exists"}),
            400,
        )

    new_admin = Admin(username=username, email=email, password=password)

    try:
        db.session.add(new_admin)
        db.session.commit()
        return jsonify({"admin_id": new_admin.admin_id}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while creating admin: {str(e)}")
        return (
            jsonify({"message": "An error occurred while processing your request."}),
            400,
        )


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
            return jsonify({"message": str(e)}), 500
    else:
        return jsonify({"message": "Admin not found"}), 404


# Route to get user details by ID
@app.route("/admin/<int:admin_id>", methods=["GET"])
def get_admin_by_id(admin_id):
    admin = Admin.query.get(admin_id)
    if admin:
        return jsonify({"username": admin.username, "email": admin.email}), 200
    else:
        # If the user is not found, return a 404 error
        return jsonify({"message": "Admin not found"}), 404


# Route to get user details by ID
@app.route("/admin/username/<string:username>", methods=["GET"])
def get_admin_by_username(username):
    admin = Admin.query.filter_by(username=username).first()
    if admin:
        return jsonify(admin.serialize()), 200
    else:
        return jsonify({"message": "Admin not found"}), 404


# Run the application
if __name__ == "__main__":
    # Set host to '0.0.0.0' to make the app accessible from other containers
    app.run(host="0.0.0.0", port=5010, debug=True)
