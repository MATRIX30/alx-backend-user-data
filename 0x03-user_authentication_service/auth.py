#!/usr/bin/env python3
"""
Module to handle user authentication
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


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


def _generate_uuid() -> str:
    """
    generates a new string UUID
    """
    return str(uuid.uuid4())


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
            hashed_password = _hash_password(password).decode('utf-8')
            new_user = User()
            self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        checks if a login is valid or not
        Args:
            email(str): users email
            password(str): users password
        Returns:
                bool: True if password is correct and False otherwise
        """
        if type(email) != str or type(password) != str:
            return False
        if len(email) == 0 or len(password) == 0:
            return False
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password):
                return True
            else:
                return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """
        creates a session based on the users email
        Args:
            email(str): the users email for which a session is to be
                        created for
        Returns:
            str: Session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
