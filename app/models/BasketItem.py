from app import db
from datetime import datetime


class BasketItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', backref=db.backref('basket_items', lazy=True))
    user = db.relationship('User', backref=db.backref('basket_items', lazy=True))

    def __repr__(self):
        return f"<BasketItem {self.product.name} - Quantity: {self.quantity}>"

    def serialize(self):
        return {
            'id': self.id,
            'product': self.product.serialize(),  # Serialize the associated product
            'user_id': self.user_id,
            'quantity': self.quantity,
            'added_at': self.added_at.isoformat()  # Serialize the datetime to a string
        }