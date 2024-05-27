#!/usr/bin/python3

"""API endpoints for places reviews"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_of_a_place(place_id):
    "Returns all reviews from storage"
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]

    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_single_review(review_id):
    """Returns a single review"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_single_review(review_id):
    """Deletes the review with the given id"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({})


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new review"""

    new_review_kwargs = request.get_json(silent=True)

    if not new_review_kwargs:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    compulsory_review_attributes = ["user_id", "text"]

    for attr in compulsory_review_attributes:
        if new_review_kwargs.get(attr) is None:
            return make_response(jsonify(
                {"error": "Missing {}".format(attr)}), 400)

    place_to_add_review_to = storage.get(Place, place_id)

    if not place_to_add_review_to:
        abort(404)

    user_adding_review = storage.get(User, new_review_kwargs["user_id"])

    if not user_adding_review:
        abort(404)

    new_review_kwargs["place_id"] = place_id

    new_review_object = Review(**new_review_kwargs)
    new_review_object.save()

    return jsonify(new_review_object.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a review"""

    review_to_update_kwargs = request.get_json(silent=True)

    if not review_to_update_kwargs:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    review_to_update = storage.get(Review, review_id)

    if review_to_update is None:
        abort(404)

    non_updatable_review_attributes = [
        "id",
        "user_id",
        "place_id",
        "created_at",
        "updated_at"
    ]

    for key, value in review_to_update_kwargs.items():
        if key not in non_updatable_review_attributes:
            setattr(review_to_update, key, value)

    storage.save()

    return jsonify(review_to_update.to_dict())
