
from flask import Blueprint, request, jsonify
from datetime import datetime
from aldo.extensions import db
from aldo.models.notifications import Notification
from aldo.models.user_accounts import User  # Assuming there is a User model with user_id
from flask_jwt_extended import jwt_required, get_jwt_identity

notification_bp = Blueprint('notification', __name__, url_prefix='/api/v1/notification')

@notification_bp.route('/', methods=['POST'])
@jwt_required()
def create_notification():
    try:
        # Extract notification data from request JSON
        data = request.json
        
        recipient_id = data.get('recipient_id')
        message = data.get('message')
        status = data.get('status', 'unread')

        # Basic input validation
        if not all([recipient_id, message]):
            return jsonify({"error": "Recipient ID and message are required"}), 400

        # Check if recipient user exists
        recipient = User.query.get(recipient_id)
        if not recipient:
            return jsonify({"error": "Recipient not found"}), 404

        # Create a new notification
        new_notification = Notification(
            recipient_id=recipient_id,
            message=message,
            created_at=datetime.now(),
            status=status
        )

        # Add notification to the database and commit
        db.session.add(new_notification)
        db.session.commit()

        return jsonify({'message': 'Notification created successfully', 'notification_id': new_notification.notification_id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@notification_bp.route('/<int:notification_id>', methods=['GET'])
@jwt_required()
def get_notification(notification_id):
    try:
        # Get notification by ID
        notification = Notification.query.get(notification_id)
        
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404
        
        # Ensure the current user is the recipient of the notification
        current_user_id = get_jwt_identity()
        if notification.recipient_id != current_user_id:
            return jsonify({'error': 'You are not authorized to view this notification'}), 403

        # Convert notification object to dictionary for response
        notification_data = {
            'notification_id': notification.notification_id,
            'recipient_id': notification.recipient_id,
            'message': notification.message,
            'created_at': notification.created_at,
            'status': notification.status
        }

        return jsonify(notification_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notification_bp.route('/<int:notification_id>', methods=['PUT'])
@jwt_required()
def update_notification(notification_id):
    try:
        # Get notification by ID
        notification = Notification.query.get(notification_id)

        if not notification:
            return jsonify({'error': 'Notification not found'}), 404

        # Ensure the current user is the recipient of the notification
        current_user_id = get_jwt_identity()
        if notification.recipient_id != current_user_id:
            return jsonify({'error': 'You are not authorized to update this notification'}), 403

        # Extract notification data from request JSON
        data = request.json

        # Update notification fields if provided in request
        if 'message' in data:
            notification.message = data['message']
        if 'status' in data:
            notification.status = data['status']

        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': 'Notification updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@notification_bp.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    try:
        # Get notification by ID
        notification = Notification.query.get(notification_id)

        if not notification:
            return jsonify({'error': 'Notification not found'}), 404

        # Ensure the current user is the recipient of the notification
        current_user_id = get_jwt_identity()
        if notification.recipient_id != current_user_id:
            return jsonify({'error': 'You are not authorized to delete this notification'}), 403

        # Delete notification from the database
        db.session.delete(notification)
        db.session.commit()

        return jsonify({'message': 'Notification deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Example route to list all notifications for the current user
@notification_bp.route('/user_notifications', methods=['GET'])
@jwt_required()
def get_user_notifications():
    try:
        # Get the current user ID from JWT token
        current_user_id = get_jwt_identity()

        # Retrieve all notifications for the current user
        notifications = Notification.query.filter_by(recipient_id=current_user_id).all()

        # Convert notifications to list of dictionaries for response
        notifications_data = [
            {
                'notification_id': notification.notification_id,
                'recipient_id': notification.recipient_id,
                'message': notification.message,
                'created_at': notification.created_at,
                'status': notification.status
            } for notification in notifications
        ]

        return jsonify(notifications_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
