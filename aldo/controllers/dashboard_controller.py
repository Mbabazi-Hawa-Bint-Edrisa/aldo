from flask import Blueprint, jsonify
from aldo.decorators import admin_required  # Assuming you have a custom decorator for admin access
from aldo.models.user_accounts import User
from aldo.models.travel_packages import TravelPackage
from aldo.models.booking import Booking
from aldo.models.payments import Payment
from aldo.models.notifications import Notification

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def admin_dashboard():
    try:
        # Example logic to fetch data for the admin dashboard
        users_count = User.query.count()
        travel_packages_count = TravelPackage.query.count()
        bookings_count = Booking.query.count()
        payments_count = Payment.query.count()
        notifications_count = Notification.query.count()

        dashboard_data = {
            'users_count': users_count,
            'travel_packages_count': travel_packages_count,
            'bookings_count': bookings_count,
            'payments_count': payments_count,
            'notifications_count': notifications_count
        }

        return jsonify(dashboard_data), 200

    except Exception as e:
        return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    try:
        users = User.query.all()
        users_data = [{'user_id': user.user_id, 'username': user.username, 'email': user.email, 'is_admin': user.is_admin} for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

@admin_bp.route('/travel_packages', methods=['GET'])
@admin_required
def get_all_travel_packages():
    try:
        travel_packages = TravelPackage.query.all()
        travel_packages_data = [{'id': package.id, 'name': package.name, 'description': package.description} for package in travel_packages]
        return jsonify(travel_packages_data), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

@admin_bp.route('/booking', methods=['GET'])
@admin_required
def get_all_bookings():
    try:
        bookings = Booking.query.all()
        bookings_data = [{'booking_id': booking.booking_id, 'user_id': booking.user_id, 'package_id': booking.package_id, 'status': booking.status} for booking in bookings]
        return jsonify(bookings_data), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

@admin_bp.route('/payments', methods=['GET'])
@admin_required
def get_all_payments():
    try:
        payments = Payment.query.all()
        payments_data = [{'payment_id': payment.payment_id, 'booking_id': payment.booking_id, 'amount': payment.amount, 'status': payment.status} for payment in payments]
        return jsonify(payments_data), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500

@admin_bp.route('/notifications', methods=['GET'])
@admin_required
def get_all_notifications():
    try:
        notifications = Notification.query.all()
        notifications_data = [{'notification_id': notification.notification_id, 'recipient_id': notification.recipient_id, 'message': notification.message, 'status': notification.status} for notification in notifications]
        return jsonify(notifications_data), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error: ' + str(e)}), 500
