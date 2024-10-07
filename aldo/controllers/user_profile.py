from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from aldo.models.user_accounts import User
from aldo.models.booking import Booking

user_profile_bp = Blueprint('user_profile', __name__, url_prefix='/api/profile')

# Get user profile data
@user_profile_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    try:
        # Fetch the current user identity from the JWT token
        current_user_id = get_jwt_identity()
        
        # Ensure that the requesting user is accessing their own profile
        if str(current_user_id) != str(user_id):
            return jsonify({"error": "You are not authorized to view this profile"}), 403
        
        # Fetch the user details
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Fetch the bookings related to the user
        bookings = Booking.query.filter_by(user_id=user_id).all()
        booking_details = [
            {
                'booking_id': booking.booking_id,
                'package_id': booking.package_id,
                'booking_date': booking.booking_date,
                'status': booking.status
            } for booking in bookings
        ]

        # Prepare the user profile data to return
        user_profile_data = {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'contact': user.contact,
            'bookings': booking_details
        }

        return jsonify(user_profile_data), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
