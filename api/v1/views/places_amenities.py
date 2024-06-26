#!/usr/bin/python3

"""
Handles all default RESTful API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"], strict_slashes=False)
def get_place_amenities(place_id):
    """Gets amenities belonging to a place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]

    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    """Unlink an amenity object from a place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if storage_t == "db":
        if amenity not in place.amenities:
            abort(404)

        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)

        place.amenity_ids.remove(amenity_id)

    storage.save()

    return (jsonify({}))


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def add_amenity_to_place(place_id, amenity_id):
    """Adds an amenity to place"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if storage_t == "db":
        if amenity not in place.amenities:
            place.amenities.append(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            place.amenity_ids.append(amenity_id)

    storage.save()

    return jsonify(amenity.to_dict())
