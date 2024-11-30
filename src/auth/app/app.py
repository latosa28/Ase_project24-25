import logging
from flask import Flask

from api.others import others_api
from api.admin import admin_api
from api.user import user_api
from errors.error_handler import register_errors
from utils_helpers.config import load_config

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

def setup():
    load_config(app)
    register_errors(app)

setup()
app.register_blueprint(user_api)
app.register_blueprint(admin_api)
app.register_blueprint(others_api)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
