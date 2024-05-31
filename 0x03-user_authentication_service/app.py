#!/usr/bin/env python3
"""
main authentication flask service
"""

from flask import Flask
from flask import jsonify


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """home route"""
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
