#!/usr/bin/python3

"""API for citys"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_of_a_state(state_id):
    "Returns all citys from storage"
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]

    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_single_city(city_id):
    """Returns a single city"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_single_city(city_id):
    """Deletes the city with the given id"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a new city"""

    new_city_kwargs = request.get_json(silent=True)

    if not new_city_kwargs:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in new_city_kwargs:
        return make_response(jsonify({"error": "Missing name"}), 400)

    state_to_add_city_to = storage.get(State, state_id)

    if not state_to_add_city_to:
        abort(404)

    new_city_kwargs["state_id"] = state_id

    new_city_object = City(**new_city_kwargs)
    new_city_object.save()

    return jsonify(new_city_object.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates a city"""

    city_to_update_kwargs = request.get_json(silent=True)

    if not city_to_update_kwargs:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    city_to_update = storage.get(City, city_id)

    if city_to_update is None:
        abort(404)

    for key, value in city_to_update_kwargs.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city_to_update, key, value)

    storage.save()

    return jsonify(city_to_update.to_dict())
