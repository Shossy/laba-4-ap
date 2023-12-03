from flask_login import login_required

from app.routes.users import bp
from flask import request, jsonify

from app.services.user_service import register_user, login, logout


@bp.route('/login/', methods=['POST'])
def login_user():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid request. Please provide a username and password.'}), 400

    username = data['username']
    password = data['password']

    try:
        user = login(username, password)
        return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401


@bp.route('/register/', methods=['POST'])
def register():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid request. Please provide a username and password.'}), 400

    username = data['username']
    password = data['password']

    try:
        new_user = register_user(username, password)
        return jsonify({'message': 'User registered successfully', 'user_id': new_user.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/logout/', methods=['POST'])
@login_required
def logout_user():
    logout()
    return jsonify({"message": " Successfuly logged out"})
