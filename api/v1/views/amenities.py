#!/usr/bin/python3

"""API for amenitys"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities():
    "Returns all amenities from storage"
    amenities = storage.all(Amenity)

    all_amenities = [amenity.to_dict() for amenity in amenities.values()]

    return jsonify(all_amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_single_amenity(amenity_id):
    """Returns a single amenity"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_single_amenity(amenity_id):
    """Deletes the amenity with the given id"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return jsonify({})


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def create_amenity():
    """Creates a new amenity"""

    new_amenity_kwargs = request.get_json(silent=True)

    if not new_amenity_kwargs:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in new_amenity_kwargs:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_amenity_object = Amenity(**new_amenity_kwargs)
    new_amenity_object.save()

    return jsonify(new_amenity_object.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an amenity"""

    amenity_to_update_kwargs = request.get_json(silent=True)

    if not amenity_to_update_kwargs:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    amenity_to_update = storage.get(Amenity, amenity_id)

    if amenity_to_update is None:
        abort(404)

    for key, value in amenity_to_update_kwargs.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity_to_update, key, value)

    storage.save()

    return jsonify(amenity_to_update.to_dict())
