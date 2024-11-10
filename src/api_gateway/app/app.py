from flask import Flask

from app.services.account.routes import account_bp
from app.services.authentication.routes import auth_bp
from app.services.collection.routes import collection_bp
from app.services.market.routes import market_bp

app_ = Flask(__name__)

# Register blueprints with their respective URL prefix
app_.register_blueprint(auth_bp, url_prefix='/auth')  # Auth routes
app_.register_blueprint(account_bp, url_prefix='/account')  # Account routes
app_.register_blueprint(collection_bp, url_prefix='/collection')  # Collection routes
app_.register_blueprint(market_bp, url_prefix='/market')  # Market routes

# Run the app
if __name__ == '__main__':
    app_.run(host='0.0.0.0', port=5000, debug=True)
