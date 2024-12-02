from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

    def serialize(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
        }
