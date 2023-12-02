from flask import Blueprint

bp = Blueprint('baskets', __name__)

from app.routes.baskets import routes
