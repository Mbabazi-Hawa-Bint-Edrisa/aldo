from flask import Blueprint, jsonify
from aldo.extensions import db
from aldo.models.user_accounts import User
from aldo.models.booking import Booking
from aldo.models.travel_packages import TravelPackage
from aldo.models.message import Message
from flask_jwt_extended import jwt_required, get_jwt_identity
from aldo.decorators import admin_required
import json

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/v1/dashboard')

@dashboard_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    try:
        users = User.query.all()
        users_data = [
            {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'contact': user.contact,
                'is_admin': user.is_admin,
                'created_at': user.created_at
            } for user in users
        ]
        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/bookings', methods=['GET'])
@jwt_required()
@admin_required
def get_all_bookings():
    try:
        bookings = Booking.query.all()
        bookings_data = [
            {
                'booking_id': booking.booking_id,
                'package_id': booking.package_id,
                'user_id': booking.user_id,
                'booking_date': booking.booking_date,
                'status': booking.status
            } for booking in bookings
        ]
        return jsonify(bookings_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/travel-packages', methods=['GET'])
@jwt_required()
@admin_required
def get_all_travel_packages():
    try:
        travel_packages = TravelPackage.query.all()
        travel_packages_data = [
            {
                'package_id': travel_package.package_id,
                'package_name': travel_package.package_name,
                'description': travel_package.description,
                'destinations': json.loads(travel_package.destinations),
                'activities': json.loads(travel_package.activities),
                'inclusions': json.loads(travel_package.inclusions),
                'price': travel_package.price,
                'start_date': travel_package.start_date.strftime('%Y-%m-%d') if travel_package.start_date else None,
                'end_date': travel_package.end_date.strftime('%Y-%m-%d') if travel_package.end_date else None,
                'availability': travel_package.availability,
                'image_url': travel_package.image_url
            } for travel_package in travel_packages
        ]
        return jsonify(travel_packages_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/messages', methods=['GET'])
@jwt_required()
@admin_required
def get_all_messages():
    try:
        messages = Message.query.all()
        messages_data = [
            {
                'id': message.id,
                'name': message.name,
                'email': message.email,
                'message': message.message,
                'created_at': message.created_at
            } for message in messages
        ]
        return jsonify(messages_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
