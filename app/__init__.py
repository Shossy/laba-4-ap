from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Create the Flask application
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object('app.config.Config')

# Initialize the SQLAlchemy database


bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

from app.models import User, Product, BasketItem

# Import and register blueprints (routes)
# from app.routes.product_routes import product_bp
# from app.routes.order_routes import order_bp
# from app.routes.user_routes import user_bp

# app.register_blueprint(product_bp, url_prefix='/api/products')
# app.register_blueprint(order_bp, url_prefix='/api/orders')
# app.register_blueprint(user_bp, url_prefix='/api/users')


if __name__ == "__main__":
    # Run the application
    app.run(debug=True)
