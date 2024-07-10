from flask import Blueprint, jsonify, request
from aldo.extensions import db, bcrypt
from aldo.models.user_accounts import User
from aldo.decorators import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token

user_bp = Blueprint('user', __name__, url_prefix='/api')

# User registration route
@user_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        contact = data.get('contact')
        password = data.get('password')

        if not username or not email or not contact or not password:
            return jsonify({"error": "All fields are required"}), 400

        if len(password) < 6:
            return jsonify({"error": "Your password must have at least 6 characters"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "This email is already registered"}), 400

        if User.query.filter_by(contact=contact).first():
            return jsonify({"error": "This contact is already registered"}), 400

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, contact=contact, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# User login route
@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid email or password'}), 401

        access_token = create_access_token(identity=str(user.user_id))
        refresh_token = create_refresh_token(identity=str(user.user_id))

        return jsonify({'message': 'Login successful',
                        'access_token': access_token,
                        'refresh_token': refresh_token}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Refresh token route
@user_bp.route('/refresh', methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user_id = get_jwt_identity()
        access_token = create_access_token(identity=current_user_id)
        return jsonify({'access_token': access_token}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Edit user route
@user_bp.route('/edit/<int:user_id>', methods=["PUT"])
@jwt_required()
def edit_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        if str(current_user_id) != str(user_id):
            return jsonify({'error': 'You are not authorized to perform this action'}), 403

        data = request.json
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'contact' in data:
            user.contact = data['contact']

        db.session.commit()

        return jsonify({'message': 'User updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete user route
@user_bp.route('/delete/<int:user_id>', methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        if str(current_user_id) != str(user_id):
            return jsonify({'error': 'You are not authorized to perform this action'}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get user profile route
@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    user_data = {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "contact": user.contact,
        "is_admin": user.is_admin
    }
    return jsonify(user_data), 200

# Admin-specific routes
@user_bp.route('/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    users = User.query.all()
    users_data = [{"user_id": user.user_id, "username": user.username, "email": user.email, "contact": user.contact, "is_admin": user.is_admin} for user in users]
    return jsonify(users_data), 200

@user_bp.route('/admin/user/<int:user_id>', methods=['GET'])
@admin_required
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    user_data = {
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "contact": user.contact,
        "is_admin": user.is_admin
    }
    return jsonify(user_data), 200

# Admin promotion route
@user_bp.route('/admin/promote/<int:user_id>', methods=['POST'])
@admin_required
def promote_to_admin(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    user.is_admin = True
    db.session.commit()

    return jsonify({"msg": "User promoted to admin successfully"}), 200

# Register the blueprint in your app
from flask import Flask

app = Flask(__name__)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run()


