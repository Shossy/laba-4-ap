from flask import Flask, request, render_template, jsonify, redirect, url_for, send_file
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from flask_login import LoginManager, current_user, login_required

from flask_admin import Admin, AdminIndexView

from flask_swagger_ui import get_swaggerui_blueprint

import requests

# Create the Flask application
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object('app.config.Config')

SWAGGER_URL = '/swagger'
API_URL = '/docs/swagger'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "store_ap"
    }
)


@app.route('/docs/swagger')
def docs():
    return send_file('openapi.json', mimetype='application/json')


# Initialize the SQLAlchemy database


bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager(app)

from app.services.user_service import login, logout
from app.models.User import User
from app.models.Product import Product
from app.models.BasketItem import BasketItem

# Import and register blueprints (routes)
from app.routes.baskets import bp as basket_bp
from app.routes.users import bp as user_bp
from app.routes.products import bp as product_bp

app.register_blueprint(basket_bp, url_prefix='/api/basket')
app.register_blueprint(product_bp, url_prefix='/api/products')
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        # Customize the access control logic based on your requirements
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to login page if not authenticated or not the admin user
        return redirect(url_for('log_user'))


admin = Admin(app, name='Store', template_mode='bootstrap3', index_view=MyAdminIndexView())


class AuthModelView(ModelView):
    @login_required
    def is_accessible(self):
        # Customize the access control logic based on your requirements
        return current_user.is_authenticated and current_user.admin


admin.add_view(AuthModelView(User, db.session, name='Users'))
admin.add_view(AuthModelView(Product, db.session, name='Products'))


@app.route('/', methods=['GET'])
def index():
    api_url = 'http://127.0.0.1:5000/api/products/'
    response = requests.get(api_url)
    print(response)

    if response.status_code == 200:
        products = response.json()
    else:
        # Handle the error, e.g., by setting products to an empty list
        products = []

    return render_template('index.html', products=products['products'])


@app.route('/cart/', methods=['GET'])
def cart():
    return render_template('cart.html')


# @app.route('/basket', methods=['GET'])
# def index():
#     api_url = 'http://127.0.0.1:5000/api/basket/get_basket'
#     response = requests.get(api_url)
#
#     if response.status_code == 200:
#         products = response.json()
#     else:
#         # Handle the error, e.g., by setting products to an empty list
#         products = []
#
#     return render_template('index.html', products=products['products'])


@app.route('/login/', methods=['GET'])
def log():
    return render_template('new login.html')


@app.route('/register/', methods=['GET'])
def reg():
    return render_template('register.html')



@app.route('/logout/', methods=['GET'])
def lout_user():
    logout()
    return jsonify({'message': 'successfully logged out'}), 201



if __name__ == "__main__":
    # Run the application
    app.run(debug=True)
