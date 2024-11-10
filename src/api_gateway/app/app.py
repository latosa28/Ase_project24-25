from flask import Flask

from api_gateway.app.services.account.routes import account_bp
from api_gateway.app.services.authentication.routes import auth_bp
from api_gateway.app.services.collection.routes import collection_bp
from api_gateway.app.services.market.routes import market_bp

app = Flask(__name__)

# Register blueprints with their respective URL prefix
app.register_blueprint(auth_bp, url_prefix='/auth')  # Auth routes
app.register_blueprint(account_bp, url_prefix='/account')  # Account routes
app.register_blueprint(collection_bp, url_prefix='/collection')  # Collection routes
app.register_blueprint(market_bp, url_prefix='/market')  # Market routes

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
