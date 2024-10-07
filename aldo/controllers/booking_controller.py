from flask import Blueprint, request, jsonify
from datetime import datetime
from aldo.extensions import db
from aldo.models.booking import Booking
from aldo.models.user_accounts import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

booking_bp = Blueprint('booking', __name__, url_prefix='/api/v1/booking')

# Create a new booking
@booking_bp.route('/create', methods=['POST'])
@jwt_required()
def create_booking():
    try:
        data = request.json

        # Get booking details from request data
        payment_method = data.get('payment_method')
        booking_source = data.get('booking_source', 'Website')
        user_id = get_jwt_identity()

        # Validate required fields
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400

        # Ensure user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Create a new booking
        new_booking = Booking(
            payment_method=payment_method,
            booking_source=booking_source,
            booking_date=datetime.now(),
            user_id=user_id
        )

        # Save to database
        db.session.add(new_booking)
        db.session.commit()

        return jsonify({'message': 'Booking created successfully', 'booking_id': new_booking.booking_id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get booking by ID
@booking_bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    try:
        booking = Booking.query.get(booking_id)

        # Validate booking exists
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        # Get current user ID
        current_user_id = get_jwt_identity()

        # Ensure user is authorized to view the booking
        if booking.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access to this booking'}), 403

        # Return booking details
        booking_data = {
            'booking_id': booking.booking_id,
            'payment_method': booking.payment_method,
            'booking_source': booking.booking_source,
            'booking_date': booking.booking_date,
            'user_id': booking.user_id
        }

        return jsonify(booking_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update a booking
@booking_bp.route('/<int:booking_id>', methods=['PUT'])
@jwt_required()
def update_booking(booking_id):
    try:
        booking = Booking.query.get(booking_id)

        # Validate booking exists
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        current_user_id = get_jwt_identity()

        # Ensure user is authorized to update the booking
        if booking.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access to this booking'}), 403

        data = request.json

        # Update booking fields
        if 'payment_method' in data:
            booking.payment_method = data['payment_method']
        if 'booking_source' in data:
            booking.booking_source = data['booking_source']

        db.session.commit()

        return jsonify({'message': 'Booking updated successfully'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a booking
@booking_bp.route('/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def delete_booking(booking_id):
    try:
        booking = Booking.query.get(booking_id)

        # Validate booking exists
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        current_user_id = get_jwt_identity()

        # Ensure user is authorized to delete the booking
        if booking.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access to this booking'}), 403

        db.session.delete(booking)
        db.session.commit()

        return jsonify({'message': 'Booking deleted successfully'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get all bookings for the current user
@booking_bp.route('/my_bookings', methods=['GET'])
@jwt_required()
def get_my_bookings():
    try:
        current_user_id = get_jwt_identity()

        # Get bookings for the current user
        bookings = Booking.query.filter_by(user_id=current_user_id).all()

        bookings_data = [
            {
                'booking_id': booking.booking_id,
                'payment_method': booking.payment_method,
                'booking_source': booking.booking_source,
                'booking_date': booking.booking_date
            } for booking in bookings
        ]

        return jsonify(bookings_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
# from flask import Blueprint, request, jsonify
# from datetime import datetime
# from aldo.extensions import db
# from aldo.models.booking import Booking

# from flask_jwt_extended import jwt_required, get_jwt_identity
# from aldo.models.user_accounts import User
# from twilio.rest import Client
# from sqlalchemy.exc import SQLAlchemyError
# from twilio.base.exceptions import TwilioRestException
# import os

# booking_bp = Blueprint('Booking', __name__, url_prefix='/api/v1/booking')

# # Twilio configuration
# account_sid = os.getenv('TWILIO_ACCOUNT_SID')
# auth_token = os.getenv('TWILIO_AUTH_TOKEN')
# twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
# client = Client(account_sid, auth_token)

# @booking_bp.route('/register', methods=['POST'])
# @jwt_required()
# def create_booking():
#     try:
#         data = request.json

#         package_id = data.get('package_id')
#         payment_method = data.get('payment_method')
#         booking_source = data.get('booking_source', 'Website')
#         user_id = get_jwt_identity()

#         if not all([package_id, payment_method, user_id]):
#             return jsonify({"error": "All required fields must be provided"}), 400

#         try:
#             package_id = int(package_id)
#         except ValueError:
#             return jsonify({"error": "Invalid package_id"}), 400

#         valid_payment_methods = ["Credit Card", "Mobile Money"]
#         if payment_method not in valid_payment_methods:
#             return jsonify({"error": "Invalid payment_method. Allowed values are: 'Credit Card', 'Mobile Money'"}), 400

#         if booking_source != 'Website':
#             return jsonify({"error": "Invalid booking_source. Allowed value is: 'Website'"}), 400

#         # package = TravelPackage.query.get(package_id)
#         # if not package:
#         #     return jsonify({'error': 'Invalid package_id'}), 400

#         user = User.query.get(user_id)
#         if not user:
#             return jsonify({'error': 'Invalid user ID'}), 400

#         new_booking = Booking(
#             package_id=package_id,
#             payment_method=payment_method,
#             booking_source=booking_source,
#             booking_date=datetime.now(),
#             user_id=user_id
#         )

#         try:
#             db.session.add(new_booking)
#             db.session.commit()
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             return jsonify({'error': 'Database error: ' + str(e)}), 500

#         if user.contact:
#             try:
#                 client.messages.create(
#                     body=f"Dear {user.username}, you have successfully booked the package '{package.package_name}'.",
#                     from_=twilio_phone_number,
#                     to=user.contact
#                 )
#             except TwilioRestException as e:
#                 return jsonify({'error': 'Twilio error: ' + str(e)}), 500

#         return jsonify({'message': 'Booking created successfully', 'booking_id': new_booking.booking_id}), 201

#     except Exception as e:
#         return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

# @booking_bp.route('/<int:booking_id>', methods=['GET'])
# @jwt_required()
# def get_booking(booking_id):
#     try:
#         booking = Booking.query.get(booking_id)
        
#         if not booking:
#             return jsonify({'error': 'Booking not found'}), 404
        
#         current_user_id = get_jwt_identity()
#         if booking.user_id != current_user_id:
#             return jsonify({'error': 'You are not authorized to view this booking'}), 403

#         booking_data = {
#             'booking_id': booking.booking_id,
#             'package_id': booking.package_id,
#             'payment_method': booking.payment_method,
#             'booking_source': booking.booking_source,
#             'booking_date': booking.booking_date,
#             'user_id': booking.user_id
#         }

#         return jsonify(booking_data), 200

#     except Exception as e:
#         return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

# @booking_bp.route('/<int:booking_id>', methods=['PUT'])
# @jwt_required()
# def update_booking(booking_id):
#     try:
#         booking = Booking.query.get(booking_id)

#         if not booking:
#             return jsonify({'error': 'Booking not found'}), 404

#         current_user_id = get_jwt_identity()
#         if booking.user_id != current_user_id:
#             return jsonify({'error': 'You are not authorized to update this booking'}), 403

#         data = request.json

#         if 'package_id' in data:
#             package_id = data['package_id']
#             package = TravelPackage.query.get(package_id)
#             if not package:
#                 return jsonify({'error': 'Invalid package_id'}), 400
#             booking.package_id = package_id

#         if 'payment_method' in data:
#             booking.payment_method = data['payment_method']
#         if 'booking_source' in data:
#             booking.booking_source = data['booking_source']

#         db.session.commit()

#         return jsonify({'message': 'Booking updated successfully'}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

# @booking_bp.route('/<int:booking_id>', methods=['DELETE'])
# @jwt_required()
# def delete_booking(booking_id):
#     try:
#         booking = Booking.query.get(booking_id)

#         if not booking:
#             return jsonify({'error': 'Booking not found'}), 404

#         current_user_id = get_jwt_identity()
#         if booking.user_id != current_user_id:
#             return jsonify({'error': 'You are not authorized to delete this booking'}), 403

#         db.session.delete(booking)
#         db.session.commit()

#         return jsonify({'message': 'Booking deleted successfully'}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

# @booking_bp.route('/user_bookings', methods=['GET'])
# @jwt_required()
# def get_user_bookings():
#     try:
#         current_user_id = get_jwt_identity()

#         user = User.query.get(current_user_id)
#         if not user:
#             return jsonify({'error': 'User not found'}), 404

#         bookings = Booking.query.filter_by(user_id=current_user_id).all()

#         bookings_data = [
#             {
#                 'booking_id': booking.booking_id,
#                 'package_id': booking.package_id,
#                 'payment_method': booking.payment_method,
#                 'booking_source': booking.booking_source,
#                 'booking_date': booking.booking_date,
#                 'user_id': booking.user_id
#             } for booking in bookings
#         ]

#         return jsonify(bookings_data), 200

#     except Exception as e:
#         return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

