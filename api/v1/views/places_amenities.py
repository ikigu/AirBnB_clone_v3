#!/usr/bin/python3

"""
Handles all default RESTful API actions
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage, storage_t
from models.city import City
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
