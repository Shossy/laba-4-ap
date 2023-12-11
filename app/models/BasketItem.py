from app import db
from datetime import datetime


class BasketItem(db.Model):
    __tablename__ = 'basket_item'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE', onupdate='CASCADE'),
                           nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<BasketItem {self.product_id} - Quantity: {self.quantity}>"

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product': self.product.serialize(),  # Serialize the associated product
            'quantity': self.quantity,
            'added_at': self.added_at.isoformat()  # Serialize the datetime to a string
        }
