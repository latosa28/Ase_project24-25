import logging
from flask import Flask

from api.admin import admin_api
from api.user import user_api
from conf.config import load_config
from models.models import db

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


def setup():
    load_config(app)
    db.init_app(app)


setup()
app.register_blueprint(user_api)
app.register_blueprint(admin_api)


if __name__ == '__main__':
    # Set host to '0.0.0.0' to make the app accessible from other containers
    app.run(host='0.0.0.0', port=5003, debug=True)
