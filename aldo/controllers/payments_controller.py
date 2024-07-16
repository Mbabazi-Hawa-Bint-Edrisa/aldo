from flask import Blueprint, request, jsonify
from datetime import datetime
from aldo.extensions import db
from aldo.models.payments import Payment
from aldo.models.booking import Booking
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

payment_bp = Blueprint('payment', __name__, url_prefix='/api/v1/payment')

logging.basicConfig(level=logging.DEBUG)

@payment_bp.route('/', methods=['POST'])
@jwt_required()
def create_payment():
    try:
        data = request.json
        logging.debug(f"Received data: {data}")
        
        booking_id = data.get('booking_id')
        amount = data.get('amount')
        payment_method = data.get('payment_method')
        status = data.get('status', 'pending')  # Default status if not provided

        # Basic input validation
        if not all([booking_id, amount, payment_method]):
            logging.error("Missing required fields")
            return jsonify({"error": "Booking ID, amount, and payment method are required"}), 400

        # Verify booking existence and ownership
        current_user_id = get_jwt_identity()
        booking = Booking.query.filter_by(booking_id=booking_id, user_id=current_user_id).first()
        
        if not booking:
            logging.error("Booking not found or not authorized")
            return jsonify({"error": "Booking not found or you are not authorized"}), 404

        # Create new payment
        new_payment = Payment(
            booking_id=booking.booking_id,
            payment_date=datetime.now(),
            amount=amount,
            payment_method=payment_method,
            status=status
        )

        db.session.add(new_payment)
        db.session.commit()

        logging.debug(f"Payment created successfully: {new_payment.payment_id}")
        return jsonify({'message': 'Payment created successfully', 'payment_id': new_payment.payment_id}), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating payment: {e}")
        return jsonify({'error': str(e)}), 500


@payment_bp.route('/<int:payment_id>', methods=['GET'])
@jwt_required()
def get_payment(payment_id):
    try:
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        current_user_id = get_jwt_identity()
        if payment.booking.user_id != current_user_id:
            return jsonify({'error': 'You are not authorized to view this payment'}), 403

        payment_data = {
            'payment_id': payment.payment_id,
            'booking_id': payment.booking_id,
            'payment_date': payment.payment_date,
            'amount': payment.amount,
            'payment_method': payment.payment_method,
            'status': payment.status
        }

        return jsonify(payment_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@payment_bp.route('/<int:payment_id>', methods=['PUT'])
@jwt_required()
def update_payment(payment_id):
    try:
        payment = Payment.query.get(payment_id)

        if not payment:
            return jsonify({'error': 'Payment not found'}), 404

        current_user_id = get_jwt_identity()
        if payment.booking.user_id != current_user_id:
            return jsonify({'error': 'You are not authorized to update this payment'}), 403

        data = request.json

        if 'amount' in data:
            payment.amount = data['amount']
        if 'payment_method' in data:
            payment.payment_method = data['payment_method']
        if 'status' in data:
            payment.status = data['status']

        db.session.commit()

        return jsonify({'message': 'Payment updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@payment_bp.route('/<int:payment_id>', methods=['DELETE'])
@jwt_required()
def delete_payment(payment_id):
    try:
        payment = Payment.query.get(payment_id)

        if not payment:
            return jsonify({'error': 'Payment not found'}), 404

        current_user_id = get_jwt_identity()
        if payment.booking.user_id != current_user_id:
            return jsonify({'error': 'You are not authorized to delete this payment'}), 403

        db.session.delete(payment)
        db.session.commit()

        return jsonify({'message': 'Payment deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@payment_bp.route('/booking/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_payments_for_booking(booking_id):
    try:
        current_user_id = get_jwt_identity()
        booking = Booking.query.filter_by(booking_id=booking_id, user_id=current_user_id).first()
        
        if not booking:
            return jsonify({"error": "Booking not found or you are not authorized"}), 404

        payments = Payment.query.filter_by(booking_id=booking_id).all()

        payments_data = [
            {
                'payment_id': payment.payment_id,
                'booking_id': payment.booking_id,
                'payment_date': payment.payment_date,
                'amount': payment.amount,
                'payment_method': payment.payment_method,
                'status': payment.status
            } for payment in payments
        ]

        return jsonify(payments_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# from flask import Blueprint, request, jsonify
# from datetime import datetime
# from aldo.extensions import db
# from aldo.models.payments import Payment
# from aldo.models.booking import Booking
# from flask_jwt_extended import jwt_required, get_jwt_identity

# payment_bp = Blueprint('payment', __name__, url_prefix='/api/v1/payment')

# @payment_bp.route('/', methods=['POST'])
# @jwt_required()
# def create_payment():
#     try:
#         data = request.json
        
#         booking_id = data.get('booking_id')
#         amount = data.get('amount')
#         payment_method = data.get('payment_method')
#         status = data.get('status', 'pending')  # Default status if not provided

#         # Basic input validation
#         if not all([booking_id, amount, payment_method]):
#             return jsonify({"error": "Booking ID, amount, and payment method are required"}), 400

#         # Verify booking existence and ownership
#         current_user_id = get_jwt_identity()
#         booking = Booking.query.filter_by(booking_id=booking_id, user_id=current_user_id).first()
        
#         if not booking:
#             return jsonify({"error": "Booking not found or you are not authorized"}), 404

#         # Create new payment
#         new_payment = Payment(
#             booking_id=booking.booking_id,
#             payment_date=datetime.now(),
#             amount=amount,
#             payment_method=payment_method,
#             status=status
#         )

#         db.session.add(new_payment)
#         db.session.commit()

#         return jsonify({'message': 'Payment created successfully', 'payment_id': new_payment.payment_id}), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500


# @payment_bp.route('/<int:payment_id>', methods=['GET'])
# @jwt_required()
# def get_payment(payment_id):
#     try:
#         payment = Payment.query.get(payment_id)
        
#         if not payment:
#             return jsonify({'error': 'Payment not found'}), 404
        
#         current_user_id = get_jwt_identity()
#         if payment.booking.user_id != current_user_id:
#             return jsonify({'error': 'You are not authorized to view this payment'}), 403

#         payment_data = {
#             'payment_id': payment.payment_id,
#             'booking_id': payment.booking_id,
#             'payment_date': payment.payment_date,
#             'amount': payment.amount,
#             'payment_method': payment.payment_method,
#             'status': payment.status
#         }

#         return jsonify(payment_data), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# @payment_bp.route('/<int:payment_id>', methods=['PUT'])
# @jwt_required()
# def update_payment(payment_id):
#     try:
#         payment = Payment.query.get(payment_id)

#         if not payment:
#             return jsonify({'error': 'Payment not found'}), 404

#         current_user_id = get_jwt_identity()
#         if payment.booking.user_id != current_user_id:
#             return jsonify({'error': 'You are not authorized to update this payment'}), 403

#         data = request.json

#         if 'amount' in data:
#             payment.amount = data['amount']
#         if 'payment_method' in data:
#             payment.payment_method = data['payment_method']
#         if 'status' in data:
#             payment.status = data['status']

#         db.session.commit()

#         return jsonify({'message': 'Payment updated successfully'}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500


# @payment_bp.route('/<int:payment_id>', methods=['DELETE'])
# @jwt_required()
# def delete_payment(payment_id):
#     try:
#         payment = Payment.query.get(payment_id)

#         if not payment:
#             return jsonify({'error': 'Payment not found'}), 404

#         current_user_id = get_jwt_identity()
#         if payment.booking.user_id != current_user_id:
#             return jsonify({'error': 'You are not authorized to delete this payment'}), 403

#         db.session.delete(payment)
#         db.session.commit()

#         return jsonify({'message': 'Payment deleted successfully'}), 200

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500


# @payment_bp.route('/booking/<int:booking_id>', methods=['GET'])
# @jwt_required()
# def get_payments_for_booking(booking_id):
#     try:
#         current_user_id = get_jwt_identity()
#         booking = Booking.query.filter_by(booking_id=booking_id, user_id=current_user_id).first()
        
#         if not booking:
#             return jsonify({"error": "Booking not found or you are not authorized"}), 404

#         payments = Payment.query.filter_by(booking_id=booking_id).all()

#         payments_data = [
#             {
#                 'payment_id': payment.payment_id,
#                 'booking_id': payment.booking_id,
#                 'payment_date': payment.payment_date,
#                 'amount': payment.amount,
#                 'payment_method': payment.payment_method,
#                 'status': payment.status
#             } for payment in payments
#         ]

#         return jsonify(payments_data), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
