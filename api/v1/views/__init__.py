#!/usr/bin/python3

"""Initiates the views module"""

from api.v1.views.cities import *
from api.v1.views.states import *
from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint("api_v1", __name__, url_prefix='/api/v1')
