#!/usr/bin/python3

"""API for states"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    "Returns all states from storage"
    states = storage.all(State)

    all_states: list = []

    for state in states.values():
        all_states.append(state.to_dict())

    return jsonify(all_states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_single_state(state_id):
    """Returns a single state"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_single_state(state_id):
    """Deletes the state with the given id"""
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()

    return jsonify({})


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a new state"""

    new_state_kwargs = request.get_json(silent=True)

    if not new_state_kwargs:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in new_state_kwargs:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_db_object = State(**new_state_kwargs)
    new_db_object.save()

    return jsonify(new_db_object.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates a state"""

    state_to_update_kwargs = request.get_json(silent=True)

    if not state_to_update_kwargs:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    object_to_update = storage.get(State, state_id)

    if object_to_update is None:
        abort(404)

    for key, value in state_to_update_kwargs.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(object_to_update, key, value)

    storage.save()

    return jsonify(object_to_update.to_dict())
