from flask_login import login_required, current_user

from app.routes.users import bp
from flask import request, jsonify

from app.services.user_service import register_user, login, logout, delete_user, user_update


@bp.route('/', methods=['GET', 'PUT'])
@login_required
def user():
    if request.method == 'GET':
        return jsonify(current_user.serialize())
    else:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Invalid request. Please provide a username and password.'}), 400
        username = data['username']
        password = data['password']

        try:
            user_update(current_user, username, password)
            return jsonify({'message': 'successfully updated'})
        except Exception as e:
            return jsonify({'error': str(e)})


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
        if str(e) == "User doesn't exist":
            code = 404
        elif str(e) == "Invalid password":
            code = 401
        else:
            code = 400
        return jsonify({'error': str(e)}), code


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
        return jsonify({'error': str(e)}), 400


@bp.route('/logout/', methods=['POST'])
@login_required
def logout_user():
    logout()
    return jsonify({"message": "Successfully logged out"})


@bp.route('/delete/', methods=['delete'])
@login_required
def delete():
    delete_user(current_user)
    return jsonify({"message": "Deleted"})
