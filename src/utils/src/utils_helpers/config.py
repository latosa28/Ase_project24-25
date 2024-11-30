import json
import os


def load_config(app):
    with open("config.json") as config_file:
        config_data = json.load(config_file)
    app.config.update(config_data)
    flask_env = os.getenv('FLASK_ENV', 'production')
    app.config['ENV'] = flask_env
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return config_data
