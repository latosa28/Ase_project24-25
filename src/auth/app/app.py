import base64
import logging
from flask import Flask

from api.others import others_api
from api.admin import admin_api
from api.user import user_api

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


app.register_blueprint(user_api)
app.register_blueprint(admin_api)
app.register_blueprint(others_api)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
