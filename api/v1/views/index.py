#!/usr/bin/python3
"""
Defines routes for the API v1 blueprint.
"""
from api.v1.views import app_views

@app_views.route('/status')
def status():
    """Returns JSON indicating the status of the app."""
    return {"status": "OK"}
