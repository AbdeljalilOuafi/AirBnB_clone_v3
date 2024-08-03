#!/usr/bin/python3
"""Defines routes for the API v1 blueprint."""
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False, methods=["GET"])
def status():
    return {
        "status": "OK",
    }
