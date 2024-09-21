from flask import Flask, jsonify, request, abort
from dotenv import load_dotenv
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from pymongo import MongoClient, ASCENDING
from marshmallow import Schema, fields, ValidationError


app = Flask(__name__)
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
print(MONGO_URI)

client = MongoClient(MONGO_URI)


class UserSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


limiter = Limiter(
    get_remote_address,  # Limit based on the IP address of the client
    app=app,
    # Global rate limit of 100 requests per minute
    storage_uri=MONGO_URI
)


user_schema = UserSchema()


db = client["mydatabase"]
collection = db["mycollection"]
collection.create_index([("id", ASCENDING)], unique=True)


@app.route('/')
def home():
    return "MongoDB Atlas + Flask API"


@app.route('/users', methods=['GET'])
@limiter.limit("5 per minute")
def get_users():
    # Get query parameters for pagination
    try:
        page = int(request.args.get('page', 1))  # Default to page 1
        # Default to 10 results per page
        limit = int(request.args.get('limit', 10))

    except ValueError:
        return jsonify({"message": "Invalid page or limit parameter, must be an integer"}), 400

    # Calculate how many documents to skip
    skip = (page - 1) * limit

    # Get users with pagination
    users = list(collection.find({}, {'_id': False}).skip(skip).limit(limit))

    # Get total number of documents in the collection (for total pages calculation)
    total_users = collection.count_documents({})

    return jsonify({
        "users": users,
        "total_users": total_users,
        "page": page,
        "total_pages": (total_users // limit) + (1 if total_users % limit > 0 else 0)
    }), 200


@app.route('/users/<int:id>', methods=['GET'])
def get_singular_user(id):
    print(id)
    user = collection.find_one(
        {"id": id}, {'_id': False})
    print(user)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    return user


@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    try:
        validated_data = user_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    if collection.find_one({"id": validated_data["id"]}):
        return jsonify({"message": "User with this ID already exists"}), 400
    # Check if a user with the same email already exists
    if collection.find_one({"email": validated_data["email"]}):
        return jsonify({"message": "User with this email already exists"}), 400

    inserted = collection.insert_one(data)
    return jsonify({"message": "Document added", "id": str(inserted.inserted_id)}), 201


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    new_data = request.json
    try:
        validated_data = user_schema.load(new_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400
    result = collection.update_one({"id": id}, {"$set": new_data})
    if result.modified_count > 0:
        return jsonify({"message": "USER updated successfully"})
    else:
        return jsonify({"message": "No User found or nothing to update"})


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    result = collection.delete_one({"id": id})
    if result.deleted_count > 0:
        return jsonify({"message": "Document deleted successfully"})
    else:
        return jsonify({"message": "No document found"})


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error="rate limit exceeded", description=str(e.description)), 429


if __name__ == '__main__':
    app.run(debug=True)
