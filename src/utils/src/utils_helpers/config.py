import json
import os


def get_db_connection_uri(app):
    db_conf = app.config['db_conf']

    if not db_conf:
        raise ValueError(f"db_conf not found!")

    db_password = open(f'/run/secrets/{db_conf["db_password_secret"]}', 'r').read().strip()

    ca_cert = os.getenv(db_conf["ca_cert_secret"], '/run/secrets/mysql_ca_cert')
    client_cert = os.getenv(db_conf["client_cert_secret"],
                            f'/run/secrets/{db_conf["client_cert_secret"]}')
    client_key = os.getenv(db_conf["client_key_secret"], f'/run/secrets/{db_conf["client_key_secret"]}')

    sql_uri = f"mysql+pymysql://{os.getenv('DB_USER')}:{db_password}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}" \
              f"?ssl_ca={ca_cert}&ssl_cert={client_cert}&ssl_key={client_key}&ssl_verify_cert=false"

    return sql_uri


def load_config(app, db_conf=True):
    with open("config.json") as config_file:
        config_data = json.load(config_file)
    app.config.update(config_data)
    flask_env = os.getenv('FLASK_ENV', 'production')
    app.config['ENV'] = flask_env
    if db_conf:
        app.config["SQLALCHEMY_DATABASE_URI"] = get_db_connection_uri(app)
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return config_data
