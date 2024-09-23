from flask import Blueprint, request, jsonify, abort
from services.user_service import get_users_paginated, get_user_by_id, create_user, update_user, delete_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Blueprint for user routes
user_bp = Blueprint('user', __name__)
limiter = Limiter(get_remote_address)


@user_bp.route('/users', methods=['GET'])
@limiter.limit("5 per minute")
def get_users():
    page = request.args.get('page', 1)
    limit = request.args.get('limit', 10)
    return get_users_paginated(page, limit)


@user_bp.route('/users/<int:id>', methods=['GET'])
def get_singular_user(id):
    return get_user_by_id(id)


@user_bp.route('/users', methods=['POST'])
def add_user():
    data = request.json
    return create_user(data)


@user_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    return update_user(id, data)


@user_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    return delete_user(id)
