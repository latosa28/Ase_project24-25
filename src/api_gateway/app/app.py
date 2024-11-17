from flask import Flask

from app.services.account.routes import account_bp
from app.services.authentication.routes import auth_bp
from app.services.collection.routes import collection_bp
from app.services.market.routes import market_bp
from app.services.currency.routes import currency_bp

app = Flask(__name__)

# Register blueprints with their respective URL prefix
app.register_blueprint(auth_bp)  # Auth routes
app.register_blueprint(account_bp)  # Account routes
app.register_blueprint(collection_bp)  # Collection routes
app.register_blueprint(market_bp)  # Market routes
app.register_blueprint(currency_bp)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
