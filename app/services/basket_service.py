# services/basket_service.py

from app import db
from app.models.BasketItem import BasketItem
from app.models.Product import Product
from app.models.User import User


def get_basket(user_id):
    pass


def add_item_to_basket(user, product_id, quantity):
    # Check if the product exists
    product = Product.query.get(product_id)
    if not product:
        raise ValueError('Product not found.')

    # Check if the quantity is valid
    if product.quantity - int(quantity) <= 0 or product.quantity - int(quantity) >= product.quantity:
        raise ValueError('Invalid quantity.')

    # Check if the user already has the product in the basket
    existing_item = BasketItem.query.filter_by(user_id=user.id, product_id=product_id).first()
    if existing_item:
        existing_item.quantity += int(quantity)
    else:
        new_item = BasketItem(user_id=user.id, product_id=product_id, quantity=quantity)
        db.session.add(new_item)

    product.quantity -= int(quantity)
    # Commit the changes to the database
    db.session.commit()
