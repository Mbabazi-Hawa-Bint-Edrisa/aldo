from flask import Blueprint, request, jsonify
from aldo.extensions import db
from aldo.models.notifications import Notification
from flask_jwt_extended import jwt_required, get_jwt_identity
from aldo.decorators import admin_required

notification_bp = Blueprint('notification', __name__, url_prefix='/api/v1/notification')

@notification_bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
def create_notification():
    try:
        data = request.json
        
        message = data.get('message')

        if not message:
            return jsonify({"error": "Message is required"}), 400

        new_notification = Notification(
            message=message
        )

        db.session.add(new_notification)
        db.session.commit()

        return jsonify({'message': 'Notification created successfully', 'notification_id': new_notification.notification_id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/<int:notification_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_notification(notification_id):
    try:
        notification = Notification.query.get(notification_id)
        
        if not notification:
            return jsonify({'error': 'Notification not found'}), 404

        notification_data = {
            'notification_id': notification.notification_id,
            'message': notification.message
        }

        return jsonify(notification_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/<int:notification_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_notification(notification_id):
    try:
        notification = Notification.query.get(notification_id)

        if not notification:
            return jsonify({'error': 'Notification not found'}), 404

        data = request.json

        if 'message' in data:
            notification.message = data['message']

        db.session.commit()

        return jsonify({'message': 'Notification updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_notification(notification_id):
    try:
        notification = Notification.query.get(notification_id)

        if not notification:
            return jsonify({'error': 'Notification not found'}), 404

        db.session.delete(notification)
        db.session.commit()

        return jsonify({'message': 'Notification deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notification_bp.route('/all_notifications', methods=['GET'])
@jwt_required()
@admin_required
def get_all_notifications():
    try:
        notifications = Notification.query.all()

        notifications_data = [
            {
                'notification_id': notification.notification_id,
                'message': notification.message
            } for notification in notifications
        ]

        return jsonify(notifications_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
