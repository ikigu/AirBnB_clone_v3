#!/usr/bin/python3

"""API for users. Contains CRUD routes"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def users():
    "Returns all users from storage"
    users = storage.all(User)

    all_users = [user.to_dict() for user in users.values()]

    return jsonify(all_users)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_single_user(user_id):
    """Returns a single user from storage"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_single_user(user_id):
    """Deletes the user with the given id"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({})


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def create_user():
    """Creates a new user"""

    new_user_kwargs = request.get_json(silent=True)

    if not new_user_kwargs:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for attribute in ["email", "password"]:
        if attribute not in new_user_kwargs:
            return make_response(jsonify(
                {"error": "Missing {}".format(attribute)}), 400)

    new_user_object = User(**new_user_kwargs)
    new_user_object.save()

    return jsonify(new_user_object.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a user in storage"""

    user_to_update_kwargs = request.get_json(silent=True)

    if not user_to_update_kwargs:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    user_to_update = storage.get(User, user_id)

    if user_to_update is None:
        abort(404)

    for key, value in user_to_update_kwargs.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user_to_update, key, value)

    storage.save()

    return jsonify(user_to_update.to_dict())
