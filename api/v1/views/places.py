#!/usr/bin/python3

"""API for places"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_of_a_city(city_id):
    "Returns all places from storage"
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]

    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_single_place(place_id):
    """Returns a single place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_single_place(place_id):
    """Deletes the place with the given id"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new place"""

    new_place_kwargs = request.get_json(silent=True)

    if not new_place_kwargs:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for attribute in ["name", "user_id"]:
        if attribute not in new_place_kwargs:
            return make_response(jsonify(
                {"error": "Missing {}".format(attribute)}), 400)

    city_to_add_place_to = storage.get(City, city_id)

    if not city_to_add_place_to:
        abort(404)

    user_to_add_place_to = storage.get(User, new_place_kwargs["user_id"])

    if not user_to_add_place_to:
        abort(404)

    new_place_kwargs["city_id"] = city_id

    new_place_object = Place(**new_place_kwargs)
    new_place_object.save()

    return jsonify(new_place_object.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a place"""

    place_to_update_kwargs = request.get_json(silent=True)

    if not place_to_update_kwargs:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    place_to_update = storage.get(Place, place_id)

    if place_to_update is None:
        abort(404)

    non_updatable_place_attributes = [
        "id",
        "user_id",
        "city_id",
        "created_at",
        "updated_at"
    ]

    for key, value in place_to_update_kwargs.items():
        if key not in non_updatable_place_attributes:
            setattr(place_to_update, key, value)

    storage.save()

    return jsonify(place_to_update.to_dict())
