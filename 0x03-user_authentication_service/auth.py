#!/usr/bin/env python3
"""
authentication module
"""

import bcrypt
from db import DB
from db import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    method takes in string password and returns hashed bytes password
            Args:
                    password(str): the string password to hash
            Returns
                    bytes: salted hashed password using bcrypt.hashpw
    """
    if password is None:
        raise
    # ensure utf-8 encoding for password
    password = password.encode("utf-8")

    # generate salt for password
    salt = bcrypt.gensalt()

    # hashing password
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a user
        Args:
            email(str): the users email
            password(str): the users password
        Returns:
            User: the user with the above information registered
        """
        if self._db.find_user_by(email=email) is not None:
            raise ValueError(f"User {email} already exists")

        # Hash the password
        hashed_password = self._hash_password(password)

        # Create a new user
        new_user = self._db.add_user(email, hashed_password)

        # Return the new user object
        return new_user
