# services/basket_service.py

from app import db
from app.models.BasketItem import BasketItem
from app.models.Product import Product
from app.models.User import User


def get_basket(user):
    basket_items = BasketItem.query.filter_by(user_id=user.id).all()
    return basket_items


def add_item_to_basket(user, product_id, quantity):
    # Check if the product exists
    product = Product.query.get(product_id)
    if not product:
        raise ValueError('Product not found.')

    # Check if the quantity is valid
    if product.quantity - int(quantity) < 0 or product.quantity - int(quantity) >= product.quantity:
        raise ValueError('Invalid quantity.')

    # Check if the user already has the product in the basket
    existing_item = BasketItem.query.filter_by(user_id=user.id, product_id=product_id).first()
    if existing_item:
        existing_item.quantity += int(quantity)
    else:
        new_item = BasketItem(user_id=user.id, product_id=product_id, quantity=quantity)
        db.session.add(new_item)

    # Commit the changes to the database
    db.session.commit()


def remove_item_from_basket(user, product_id, quantity):
    # Check if the product exists
    product = Product.query.get(product_id)
    if not product:
        raise ValueError('Product not found.')

    # Check if the quantity is valid

    # Check if the user already has the product in the basket
    existing_item = BasketItem.query.filter_by(user_id=user.id, product_id=product_id).first()
    if existing_item:
        if existing_item.quantity == int(quantity):
            db.session.delete(existing_item)
        elif existing_item.quantity - int(quantity) > 0 and int(quantity) >= 0:
            existing_item.quantity -= int(quantity)
        else:
            raise ValueError('Invalid quantity.')
    else:
        raise ValueError("You don't have this item in basket")

    # Commit the changes to the database
    db.session.commit()


def pay_for_order(user):
    basket = get_basket(user)
    shortage = []
    for item in basket:
        if item.product.quantity < item.quantity:
            shortage.append(item.product.name)
        else:
            item.product.quantity -= item.quantity
            db.session.delete(item)

    if shortage:
        raise ValueError("We have shortage of " + ', '.join(name for name in shortage))
    db.session.commit()
