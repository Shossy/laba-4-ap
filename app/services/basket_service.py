# services/basket_service.py

from app import db
from app.models.BasketItem import BasketItem
from app.models.Product import Product


def get_basket(user):
    basket_items = user.basket_items
    return basket_items


def add_item_to_basket(user, product_id, quantity):
    # Check if the product exists
    product = Product.query.get(product_id)
    if not product:
        raise ValueError('Product not found.')

    # Check if the quantity is valid
    if product.quantity - int(quantity) < 0 or int(quantity) <= 0:
        raise ValueError('Invalid quantity.')
    # Check if the user already has the product in the basket
    existing_item = BasketItem.query.filter_by(user_id=user.id, product_id=product_id).first()
    if existing_item:
        if product.quantity - int(quantity) - existing_item.quantity < 0:
            raise ValueError('Invalid quantity.')
        existing_item.quantity += int(quantity)
    else:
        new_item = BasketItem(user_id=user.id, product_id=product_id, quantity=quantity)
        db.session.add(new_item)

    # Commit the changes to the database
    db.session.commit()


def update_quantity(user, product_id, quantity):
    # Check if the product exists
    product = Product.query.get(product_id)
    if not product:
        raise ValueError('Product not found.')

    # Check if the quantity is valid

    # Check if the user already has the product in the basket
    existing_item = BasketItem.query.filter_by(user_id=user.id, product_id=product_id).first()
    if existing_item:
        if int(quantity) == 0:
            db.session.delete(existing_item)
        elif int(quantity) > existing_item.product.quantity:
            raise ValueError("Invalid quantity")
        else:
            existing_item.quantity = int(quantity)
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

    if shortage:
        raise ValueError("We have shortage of " + ', '.join(name for name in shortage) + ". Please adjust")
    clear_basket_from_items(user)
    db.session.commit()


def clear_basket_from_items(user):
    basket = get_basket(user)
    for item in basket:
        db.session.delete(item)
    db.session.commit()
