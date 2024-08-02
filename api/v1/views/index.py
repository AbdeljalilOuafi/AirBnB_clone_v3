#!/usr/bin/python3

from api.v1.views import app_views

@app_views.route('/status')
def status():
    """return json for the status of the app"""
    return {"status": "OK"}
