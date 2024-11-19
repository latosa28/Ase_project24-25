from flask import Flask

from app.services.admin_account.routes import admin_account_bp
from app.services.authentication.routes import auth_bp
from app.services.collection.routes import collection_bp
from app.services.market.routes import market_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_account_bp)
app.register_blueprint(collection_bp)
app.register_blueprint(market_bp)


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)
