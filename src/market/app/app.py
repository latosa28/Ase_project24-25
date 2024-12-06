import logging
from flask import Flask
from api.admin import admin_api
from api.user import user_api
from errors.error_handler import register_errors
from utils_helpers.auth import AuthHelper
from helpers.scheduler import SchedulerHelper
from models.models import db
from utils_helpers.config import load_config

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


def setup():
    load_config(app)
    register_errors(app)
    db.init_app(app)
    public_key = AuthHelper.get_jwt_public_key(app.config['ENV'])
    app.config["jwt_public_key"] = public_key
    SchedulerHelper(app).start_scheduler()


setup()
app.register_blueprint(user_api)
app.register_blueprint(admin_api)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5004)
