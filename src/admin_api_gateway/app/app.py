from flask import Flask

from errors.error_handler import register_errors
from services.account.routes import account_bp
from services.admin_account.routes import admin_account_bp
from services.authentication.routes import auth_bp
from services.collection.routes import collection_bp
from services.market.routes import market_bp
from services.payment.routes import payment_bp

app = Flask(__name__)
register_errors(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_account_bp)
app.register_blueprint(account_bp)
app.register_blueprint(collection_bp)
app.register_blueprint(market_bp)
app.register_blueprint(payment_bp)


# Run the app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5010)
