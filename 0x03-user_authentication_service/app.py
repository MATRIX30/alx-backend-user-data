#!/usr/bin/env python3
"""A simple Flask app with user authentication features.
"""
import logging

from flask import Flask, abort, jsonify, redirect, request

from auth import Auth

logging.disable(logging.WARNING)


AUTH = Auth()
app = Flask(__name__)

@app.route("/", strict_slashes=False)
def index():
    """home route"""
    return jsonify({"message": "Bienvenue"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
