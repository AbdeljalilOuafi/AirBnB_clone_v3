#!/usr/bin/python3

from flask import abort, jsonify, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def get_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users", strict_slashes=False, methods=["GET"])
def get_all_users():
    users_dict = storage.all(User)
    users = []
    for user in users_dict.values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>",
                 strict_slashes=True, methods=["PUT"])
def update_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key in ["id", "email", "created_at", "updated_at"]:
            continue
        setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
