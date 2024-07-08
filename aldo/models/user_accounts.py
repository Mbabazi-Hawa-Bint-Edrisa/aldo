# models.py
from aldo.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    contact = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)  # New field to indicate admin status

    # Define the relationship with Notification model
    notifications = db.relationship('Notification', back_populates='recipient', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

# decorators.py
from functools import wraps
from flask import abort
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from aldo.models.user_accounts import User

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user is None or not user.is_admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

# routes.py
from flask import Blueprint, Flask
from aldo.decorators import admin_required  # Import the decorator

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # Your logic to display the admin dashboard
    return "Admin Dashboard"

# Register the blueprint in your app
app = Flask(__name__)
app.register_blueprint(admin_bp)

# if __name__ == '__main__':
#     app.run()


# from aldo.extensions import db

# class User(db.Model):
#     __tablename__ = 'users'

#     user_id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), nullable=False, unique=True)
#     email = db.Column(db.String(120), nullable=False, unique=True)
#     password_hash = db.Column(db.String(128), nullable=False)
#     contact = db.Column(db.String(20))

#     # Define the relationship with Notification model
#     notifications = db.relationship('Notification', back_populates='recipient', lazy=True)

#     def __repr__(self):
#         return f'<User {self.username}>'
