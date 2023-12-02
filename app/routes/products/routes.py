from app.routes.products import bp
from flask import jsonify
from app.models.Product import Product

@bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    serialized_products = [product.serialize() for product in products]
    return jsonify(products=serialized_products)

