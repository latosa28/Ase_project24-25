import logging

import requests
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

from sqlalchemy.exc import IntegrityError

# Initialize the Flask application
app = Flask(__name__)

CURRENCY_URL = "http://currency:5005"
currency_request_function = None  # Variabile globale per il mock

logging.basicConfig(level=logging.DEBUG)
# Database configuration
# The URI is dynamically set using environment variables for security
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Marshmallow for ORM and serialization
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Define the User model for the 'user' table in the database
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


# Schema for serializing the User object into JSON
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

# Funzione per effettuare la richiesta al servizio `currency`
def _make_currency_request(user_id, amount):
    if currency_request_function:
        return currency_request_function(user_id, amount)
    else:
        # Comportamento normale, esegue la richiesta reale
        return requests.post(CURRENCY_URL + f'/user/{user_id}/add_amount', json={"amount": amount})

# Route to create a new user
@app.route('/user', methods=['POST'])
def create_user():
    # Get data from the incoming JSON request
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    # Ensure all required fields are provided
    if not username or not email or not password:
        return jsonify({"message": "Missing data"}), 400

    # Check if a user with the same username or email already exists
    user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "User with this username or email already exists"}), 400

    # Create a new user instance
    new_user = User(username=username, email=email, password=password)

    try:
        db.session.add(new_user)
        db.session.commit()
        response = _make_currency_request(new_user.user_id, 500)
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
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Try to find the user by ID
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
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    # Find the user by ID
    user = User.query.get(user_id)
    if user:
        # Return the user data as JSON
        user_data = UserSchema().dump(user)  # Serializzazione corretta
        return jsonify(user_data), 200
    else:
        # If the user is not found, return a 404 error
        return jsonify({"message": "User not found"}), 404


# Route to get user details by username
@app.route('/user/username/<string:username>', methods=['GET'])
def get_user_by_username(username):
    # Find the user by username
    user = User.query.filter_by(username=username).first()
    if user:
        # Return the user data as JSON
        user_data = UserSchema().dump(user)  # Serializzazione corretta
        return jsonify(user_data), 200
    else:
        # If the user is not found, return a 404 error
        return jsonify({"message": "User not found"}), 404


# Route to get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    # Get all users from the database
    all_users = User.query.all()
    # Serialize the list of users
    user_data = users_schema.dump(all_users)
    return jsonify(user_data), 200


# Initialize Marshmallow schema for user
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Run the application
if __name__ == '__main__':
    # Set host to '0.0.0.0' to make the app accessible from other containers
    app.run(host='0.0.0.0', port=5003, debug=True)
