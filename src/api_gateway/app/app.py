from flask import Flask

from conf.config import load_config
from services.account.routes import account_bp
from services.auth.routes import auth_bp
from services.collection.routes import collection_bp
from services.currency.routes import currency_bp
from services.market.routes import market_bp
from services.payment.routes import payment_bp

app = Flask(__name__)
load_config(app)

app.register_blueprint(auth_bp)
app.register_blueprint(account_bp)
app.register_blueprint(collection_bp)
app.register_blueprint(market_bp)
app.register_blueprint(currency_bp)
app.register_blueprint(payment_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
