from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# Create the Flask application
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object('app.config.Config')

# Initialize the SQLAlchemy database


bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager(app)

from app.models import User, Product, BasketItem

# Import and register blueprints (routes)
from app.routes.baskets import bp as basket_bp
from app.routes.users import bp as user_bp
from app.routes.products import bp as product_bp

app.register_blueprint(basket_bp, url_prefix='/api/basket')
app.register_blueprint(product_bp, url_prefix='/api/products')
app.register_blueprint(user_bp, url_prefix='/api/user')


if __name__ == "__main__":
    # Run the application
    app.run(debug=True)
