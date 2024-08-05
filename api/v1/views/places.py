#!/usr/bin/python3
"""This Module implements CRUD operations for places"""
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=["GET"])
def get_city_places(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_objects = city.places
    places = []
    for place in places_objects:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def get_city(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=["POST"])
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "name" not in data:
        abort(400, "Missing name")
    user = storage.get(User, data.get("user_id"))
    if user is None:
        abort(404)
    new_place = Place(city_id=city.id, **data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>",
                 strict_slashes=False, methods=["PUT"])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            continue
        setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
