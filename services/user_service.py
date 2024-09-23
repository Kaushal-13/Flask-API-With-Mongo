from pymongo import MongoClient, ASCENDING
from marshmallow import ValidationError
from flask import jsonify
from models.user_model import user_schema
import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("MONGO_URI"))


client = MongoClient(os.getenv("MONGO_URI"))

db = client["mydatabase"]
collection = db["mycollection"]
collection.create_index([("id", ASCENDING)], unique=True)


def get_users_paginated(page, limit):
    try:
        page = int(page)
        limit = int(limit)
    except ValueError:
        return jsonify({"message": "Invalid page or limit parameter, must be an integer"}), 400

    skip = (page - 1) * limit
    users = list(collection.find({}, {'_id': False}).skip(skip).limit(limit))
    total_users = collection.count_documents({})

    return jsonify({
        "users": users,
        "total_users": total_users,
        "page": page,
        "total_pages": (total_users // limit) + (1 if total_users % limit > 0 else 0)
    }), 200


def get_user_by_id(id):
    user = collection.find_one({"id": id}, {'_id': False})
    if user is None:
        return jsonify({"message": "User not found"}), 404
    return user


def create_user(data):
    try:
        validated_data = user_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if collection.find_one({"id": validated_data["id"]}) or collection.find_one({"email": validated_data["email"]}):
        return jsonify({"message": "User with this ID or email already exists"}), 400

    inserted = collection.insert_one(validated_data)
    return jsonify({"message": "User added", "id": str(inserted.inserted_id)}), 201


def update_user(id, data):
    try:
        validated_data = user_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    result = collection.update_one({"id": id}, {"$set": validated_data})
    if result.modified_count > 0:
        return jsonify({"message": "User updated successfully"})
    return jsonify({"message": "No user found or nothing to update"})


def delete_user(id):
    result = collection.delete_one({"id": id})
    if result.deleted_count > 0:
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"message": "No user found"})
