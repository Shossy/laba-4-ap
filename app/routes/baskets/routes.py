from flask import request, jsonify
from flask_login import login_required, current_user
from app.routes.baskets import bp
from app.services.basket_service import add_item_to_basket, get_basket, remove_item_from_basket, pay_for_order


@bp.route('/', methods=['GET'])
@login_required
def get():
    basket = get_basket(current_user)
    basket_items_serialized = [basket_item.serialize() for basket_item in basket]
    return jsonify(basket_items_serialized)


@bp.route('/add_item/',  methods=['POST'])
@login_required
def add_item():
    data = request.get_json()

    if not data or 'product_id' not in data or 'quantity' not in data:
        return jsonify({'error': 'Invalid request. Please provide a product_id and quantity.'}), 400

    product_id = data['product_id']
    quantity = data['quantity']

    try:
        add_item_to_basket(current_user, product_id, quantity)
        return jsonify({'message': 'Item added to basket successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/remove_item/', methods=["POST"])
def remove_item():
    data = request.get_json()

    if not data or 'product_id' not in data or 'quantity' not in data:
        return jsonify({'error': 'Invalid request. Please provide a product_id and quantity.'}), 400

    product_id = data['product_id']
    quantity = data['quantity']
    try:
        remove_item_from_basket(current_user, product_id, quantity)
        return jsonify({'message': 'Items removed from basket successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/pay/', methods=["POST"])
@login_required
def pay():
    try:
        pay_for_order(current_user)
        return jsonify({'message': 'Payment done successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

