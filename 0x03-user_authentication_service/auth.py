#!/usr/bin/env python3
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """
    hashes a string password
    Args:
        password(str): string password to be hashed
    Returns:
        hashed_password(bytes): the hashed password hashed_password
    """
    if type(password) != str:
        return None
    encoded_password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(encoded_password, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        method to register a new user to the database
            Args:
                email(str): users email
                password(str): users password
            Returns:
                User: a newly registered user
        """
        if type(email) != str or type(password) != str:
            return None
        if len(email) <= 0 or len(password) <= 0:
            return None

        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = User()
            self._db.add_user(email, hashed_password)
            new_user.email = email
            new_user.hashed_password = hashed_password
            return new_user
