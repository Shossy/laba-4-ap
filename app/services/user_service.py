# services/user_service.py

from app import db, login_manager
from app.models.User import User
from flask_login import login_user, logout_user


def register_user(username, password):
    # Check if the username is already taken
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        raise ValueError('Username already taken. Please choose another one.')

    # Create a new user
    new_user = User(username=username)
    new_user.set_password(password)

    # Save the user to the database
    db.session.add(new_user)
    db.session.commit()

    return new_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def login(username, password):
    # Check if user exists
    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        raise ValueError("User doesn't exist")

    # Check password
    if existing_user.check_password(password=password):
        login_user(existing_user)
        return existing_user
    else:
        raise ValueError("Invalid password")


def logout():
    logout_user()
