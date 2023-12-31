from flask import request, jsonify
from flask_login import login_required, current_user
from app.routes.baskets import bp
from app.services.basket_service import add_item_to_basket, get_basket,  pay_for_order, \
    clear_basket_from_items, update_quantity


@bp.route('/', methods=['GET'])
@login_required
def get():
    basket = get_basket(current_user)
    basket_items_serialized = [basket_item.serialize() for basket_item in basket]
    return jsonify(basket_items_serialized), 200


@bp.route('/add_item', methods=['POST'])
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
        return jsonify({'error': str(e)}), 400


@bp.route('/update_item', methods=["PUT"])
def update_item():
    data = request.get_json()

    if not data or 'product_id' not in data or 'quantity' not in data:
        return jsonify({'error': 'Invalid request. Please provide a product_id and quantity.'}), 400

    product_id = data['product_id']
    quantity = data['quantity']
    try:
        update_quantity(current_user, product_id, quantity)
        return jsonify({'message': 'Item updated successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/pay', methods=["POST"])
@login_required
def pay():
    try:
        pay_for_order(current_user)
        return jsonify({'message': 'Payment done successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/clear_basket', methods=["DELETE"])
@login_required
def clear_basket():
    try:
        clear_basket_from_items(current_user)
        return jsonify({'message': 'Cleared successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
