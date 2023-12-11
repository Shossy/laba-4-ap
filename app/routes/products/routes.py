from app.routes.products import bp
from flask import jsonify, request
from app.models.Product import Product
from flask_login import current_user, login_required




@bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    serialized_products = [product.serialize() for product in products]
    return jsonify(products=serialized_products)


@bp.route('/<product_id>/', methods=['GET'])
def get_product(product_id):

    product = Product.query.where(Product.id == product_id).first()
    if product is None:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify(product.serialize())


