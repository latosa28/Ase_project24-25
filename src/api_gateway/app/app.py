from flask import Flask

from errors.error_handler import register_errors
from services.account.routes import account_bp
from services.auth.routes import auth_bp
from services.collection.routes import collection_bp
from services.currency.routes import currency_bp
from services.market.routes import market_bp
from services.payment.routes import payment_bp
from utils_helpers.config import load_config

app = Flask(__name__)
load_config(app)
register_errors(app)

app.register_blueprint(auth_bp)
app.register_blueprint(account_bp)
app.register_blueprint(collection_bp)
app.register_blueprint(market_bp)
app.register_blueprint(currency_bp)
app.register_blueprint(payment_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
