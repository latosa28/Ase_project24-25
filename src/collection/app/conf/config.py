import json
import os


def _check_rarities(rarities: dict):
    # Verifica che la somma delle percentuali sia 100
    total_percentage = sum(rarities.values())
    if total_percentage != 100.0:
        raise ValueError(
            f"Le percentuali sommano {total_percentage}. Devono essere esattamente 100."
        )


def load_config(app):
    with open("conf/config.json") as config_file:
        config_data = json.load(config_file)
    rarities = config_data.get("rarities")
    if rarities:
        _check_rarities(rarities)
    app.config.update(config_data)
    flask_env = os.getenv('FLASK_ENV', 'production')
    app.config['ENV'] = flask_env
    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
