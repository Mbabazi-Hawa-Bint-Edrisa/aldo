from flask import Blueprint, request, jsonify
from aldo.extensions import db
from aldo.models.message import Message
from flask_jwt_extended import jwt_required
from aldo.decorators import admin_required



message= Blueprint('payment', __name__, url_prefix='/api/v1/message')

@message.route('/messages', methods=['POST'])
def receive_message():
    data = request.json
    
    # Extract data from the request
    name = data.get('name')
    email = data.get('email')
    message_content = data.get('message')
    
    # Validate the data
    if not name or not email or not message_content:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create a new message instance
    new_message = Message(name=name, email=email, message=message_content)
    
    # Add and commit the new message to the database
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify({'message': 'Message received successfully'}), 201

@message.route('/messages', methods=['GET'])
def get_messages():
    # Retrieve all messages from the database
    messages = Message.query.all()
    
    # Serialize the data
    messages_list = []
    for message in messages:
        messages_list.append({
            'id': message.id,
            'name': message.name,
            'email': message.email,
            'message': message.message,
            'created_at': message.created_at
        })
    
    return jsonify(messages_list), 200


