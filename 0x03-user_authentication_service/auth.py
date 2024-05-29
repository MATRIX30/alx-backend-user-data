#!/usr/bin/env python3
"""
authentication module
"""

import bcrypt


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
