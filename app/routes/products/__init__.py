from flask import Blueprint

bp = Blueprint('products', __name__)

from app.routes.products import routes
