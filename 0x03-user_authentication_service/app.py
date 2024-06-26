#!/usr/bin/env python3
"""
main authentication flask service
"""

from flask import Flask, abort, make_response
from flask import jsonify, request
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """home route"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", strict_slashes=False, methods=["POST"])
def users():
    """route function to handle users"""
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or password is None:
        return
    if type(email) != str or type(password) != str:
        return
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", strict_slashes=False, methods=["POST"])
def login():
    """
    method to handle login
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
