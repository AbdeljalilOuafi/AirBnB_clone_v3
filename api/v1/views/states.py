#!/usr/bin/python3
"""This Module implements CRUD operations for states"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route("/states", strict_slashes=False, methods=["GET"])
@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def states(state_id=None):
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict())
    else:
        states_list = []
        states = storage.all(State)
        for obj in states.values():
            states_list.append(obj.to_dict())
        return jsonify(states_list)


@app_views.route("/states/<state_id>",
                 strict_slashes=False, methods=["DELETE"])
def del_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if data is None:
        abort(400, "Not a JSON")
    state.name = data.get("name", state.name)
    state.save()
    return jsonify(state.to_dict()), 200
