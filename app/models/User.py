from app import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)  # The hashed password will be stored

    basket_items = db.relationship('BasketItem', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User {self.username}>"

    # Example method to hash a password
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Example method to check a password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)




