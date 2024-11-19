import logging

import requests
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

from sqlalchemy.exc import IntegrityError

# Initialize the Flask application
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)
# Database configuration
# The URI is dynamically set using environment variables for security
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Marshmallow for ORM and serialization
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Define the User model for the 'user' table in the database
class Admin(db.Model):
    __tablename__ = 'admin_account'
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


# Schema for serializing the User object into JSON
class AdminSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Admin


# Route to create a new admin
@app.route('/admin', methods=['POST'])
def create_admin():
    # Get data from the incoming JSON request
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    # Ensure all required fields are provided
    if not username or not email or not password:
        return jsonify({"message": "Missing data"}), 400

    # Check if a user with the same username or email already exists
    admin = Admin.query.filter_by(username=username).first() or Admin.query.filter_by(email=email).first()
    if admin:
        return jsonify({"message": "User with this username or email already exists"}), 400

    # Create a new user instance
    new_admin = Admin(username=username, email=email, password=password)

    try:
        db.session.add(new_admin)
        db.session.commit()
        return jsonify({"admin_id": new_admin.admin_id}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while creating admin: {str(e)}")
        return jsonify({"message": "An error occurred while processing your request."}), 400


# Route to delete an existing user by ID
@app.route('/admin/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    # Try to find the user by ID
    admin = Admin.query.get(admin_id)
    if admin:
        try:
            # Delete the user and commit the changes
            db.session.delete(admin)
            db.session.commit()
            return jsonify({"message": "Admin deleted successfully"}), 200
        except Exception as e:
            # In case of an error, rollback the transaction
            db.session.rollback()
            return jsonify({"message": str(e)}), 500
    else:
        # If the user is not found, return a 404 error
        return jsonify({"message": "Admin not found"}), 404


# Route to get user details by ID
@app.route('/admin/<int:admin_id>', methods=['GET'])
def get_admin_by_id(admin_id):
    # Find the user by ID
    admin = Admin.query.get(admin_id)
    if admin:
        # Return the user data as JSON
        admin_data = AdminSchema().dump(admin)  # Serializzazione corretta
        return jsonify(admin_data), 200
    else:
        # If the user is not found, return a 404 error
        return jsonify({"message": "Admin not found"}), 404

# Route to get user details by ID
@app.route('/admin/<string:username>', methods=['GET'])
def get_admin_by_username(username):
    # Find the user by ID
    admin = Admin.query.get(username)
    if admin:
        # Return the user data as JSON
        admin_data = AdminSchema().dump(admin)  # Serializzazione corretta
        return jsonify(admin_data), 200
    else:
        # If the user is not found, return a 404 error
        return jsonify({"message": "Admin not found"}), 404



# Initialize Marshmallow schema for user
admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

# Run the application
if __name__ == '__main__':
    # Set host to '0.0.0.0' to make the app accessible from other containers
    app.run(host='0.0.0.0', port=5010, debug=True)
