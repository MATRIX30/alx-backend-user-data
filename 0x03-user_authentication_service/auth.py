#!/usr/bin/env python3
import bcrypt


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
