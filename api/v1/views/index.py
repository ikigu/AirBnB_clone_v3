#!/usr/bin/python3

"""Shared API routes. Contains status and stats"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """Status API check. Returns status of API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Returns count of each object class in the database"""

    objects = {
        "amenities": Amenity,
        "cities": City,
        "place": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }

    objects_dict: dict = {}

    for key, value in objects.items():
        objects_dict[key] = storage.count(value)

    return jsonify(objects_dict)
