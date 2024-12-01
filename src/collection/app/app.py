import logging
from flask import Flask

from conf.config import setup_config
from errors.error_handler import register_errors
from utils_helpers.auth import AuthHelper
from api.admin import admin_api
from api.user import user_api
from models.models import db

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


def setup():
    setup_config(app)
    register_errors(app)
    db.init_app(app)
    public_key = AuthHelper.get_jwt_public_key(app.config['ENV'])
    app.config["jwt_public_key"] = public_key


setup()
app.register_blueprint(user_api)
app.register_blueprint(admin_api)


# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
