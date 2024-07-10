
from flask import Blueprint, request, jsonify
from aldo.extensions import db
from aldo.models.travel_packages import TravelPackage
from flask_jwt_extended import jwt_required
import json

travel_package_bp = Blueprint('travel_package', __name__, url_prefix='/api/v1/travel_package')

# Helper function to serialize lists to JSON strings
def serialize_to_json(value):
    return json.dumps(value) if value else '[]'

# Helper function to deserialize JSON strings to lists
def deserialize_from_json(value):
    return json.loads(value) if value else []

@travel_package_bp.route('/', methods=['POST'])
@jwt_required()  # Ensure the user is authenticated
def create_travel_package():
    try:
        # Extract travel package data from request JSON
        data = request.json
        
        package_name = data.get('package_name')
        description = data.get('description')
        destinations = serialize_to_json(data.get('destinations', []))  # Serialize list to JSON
        activities = serialize_to_json(data.get('activities', []))  # Serialize list to JSON
        inclusions = serialize_to_json(data.get('inclusions', []))  # Serialize list to JSON
        price = data.get('price')
        duration = data.get('duration')
        availability = data.get('availability', True)
        image_url = data.get('image_url')

        # Basic input validation
        if not all([package_name, price, duration]):
            return jsonify({"error": "Package name, price, and duration are required"}), 400

        # Create a new travel package
        new_travel_package = TravelPackage(
            package_name=package_name,
            description=description,
            destinations=destinations,
            activities=activities,
            inclusions=inclusions,
            price=price,
            duration=duration,
            availability=availability,
            image_url=image_url
        )

        # Add the new travel package to the database and commit
        db.session.add(new_travel_package)
        db.session.commit()

        return jsonify({'message': 'Travel package created successfully', 'package_id': new_travel_package.package_id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@travel_package_bp.route('/<int:package_id>', methods=['GET'])
@jwt_required()  # Ensure the user is authenticated
def get_travel_package(package_id):
    try:
        # Get travel package by ID
        travel_package = TravelPackage.query.get(package_id)
        
        if not travel_package:
            return jsonify({'error': 'Travel package not found'}), 404

        # Convert travel package object to dictionary for response
        travel_package_data = {
            'package_id': travel_package.package_id,
            'package_name': travel_package.package_name,
            'description': travel_package.description,
            'destinations': deserialize_from_json(travel_package.destinations),  # Deserialize JSON to list
            'activities': deserialize_from_json(travel_package.activities),  # Deserialize JSON to list
            'inclusions': deserialize_from_json(travel_package.inclusions),  # Deserialize JSON to list
            'price': travel_package.price,
            'duration': travel_package.duration,
            'availability': travel_package.availability,
            'image_url': travel_package.image_url
        }

        return jsonify(travel_package_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@travel_package_bp.route('/<int:package_id>', methods=['PUT'])
@jwt_required()  # Ensure the user is authenticated
def update_travel_package(package_id):
    try:
        # Get travel package by ID
        travel_package = TravelPackage.query.get(package_id)

        if not travel_package:
            return jsonify({'error': 'Travel package not found'}), 404

        # Extract travel package data from request JSON
        data = request.json

        # Update travel package fields if provided in request
        if 'package_name' in data:
            travel_package.package_name = data['package_name']
        if 'description' in data:
            travel_package.description = data['description']
        if 'destinations' in data:
            travel_package.destinations = serialize_to_json(data['destinations'])  # Serialize list to JSON
        if 'activities' in data:
            travel_package.activities = serialize_to_json(data['activities'])  # Serialize list to JSON
        if 'inclusions' in data:
            travel_package.inclusions = serialize_to_json(data['inclusions'])  # Serialize list to JSON
        if 'price' in data:
            travel_package.price = data['price']
        if 'duration' in data:
            travel_package.duration = data['duration']
        if 'availability' in data:
            travel_package.availability = data['availability']
        if 'image_url' in data:
            travel_package.image_url = data['image_url']

        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': 'Travel package updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@travel_package_bp.route('/<int:package_id>', methods=['DELETE'])
@jwt_required()  # Ensure the user is authenticated
def delete_travel_package(package_id):
    try:
        # Get travel package by ID
        travel_package = TravelPackage.query.get(package_id)

        if not travel_package:
            return jsonify({'error': 'Travel package not found'}), 404

        # Delete travel package from the database
        db.session.delete(travel_package)
        db.session.commit()

        return jsonify({'message': 'Travel package deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Example route to list all available travel packages
@travel_package_bp.route('/', methods=['GET'])
def get_all_travel_packages():
    try:
        # Retrieve all travel packages that are available
        travel_packages = TravelPackage.query.filter_by(availability=True).all()

        # Convert travel packages to list of dictionaries for response
        travel_packages_data = [
            {
                'package_id': travel_package.package_id,
                'package_name': travel_package.package_name,
                'description': travel_package.description,
                'destinations': deserialize_from_json(travel_package.destinations),  # Deserialize JSON to list
                'activities': deserialize_from_json(travel_package.activities),  # Deserialize JSON to list
                'inclusions': deserialize_from_json(travel_package.inclusions),  # Deserialize JSON to list
                'price': travel_package.price,
                'duration': travel_package.duration,
                'availability': travel_package.availability,
                'image_url': travel_package.image_url
            } for travel_package in travel_packages
        ]

        return jsonify(travel_packages_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
