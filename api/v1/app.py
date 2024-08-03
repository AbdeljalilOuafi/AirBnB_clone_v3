#!/usr/bin/python3
"""Main application setup for the Flask API."""
from api.v1.views import app_views
from flask import Flask
import os
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """closes database storage"""
    try:
        storage.close()
    except Exception as e:
        print(f"Error closing storage: {e}")


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
