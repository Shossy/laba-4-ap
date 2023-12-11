from app import db, bcrypt


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)  # The hashed password will be stored
    admin = db.Column(db.Boolean, default=False, nullable=False)

    basket_items = db.relationship('BasketItem', backref='user', order_by='BasketItem.added_at',
                                   cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User {self.username}>"

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }

    # Example method to hash a password
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Example method to check a password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __init__(self, is_active=True):
        self.is_active = is_active

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
