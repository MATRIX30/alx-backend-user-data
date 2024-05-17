#!/usr/bin/env python3
"""
contains functions related to encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes password to byte string using hashpw function of
    bcrypt package
    Args:
                password(str): the password to hash
        Returns:
                bytes: salted hashed password
    """
    salt = bcrypt.gensalt()
    password = password.encode("utf-8")
    return bcrypt.hashpw(password, salt)


def is_valid(hsh_password: bytes, password: str) -> bool:
    """
    verify if a password corresponds to a hash value
    """
    password = password.encode("utf-8")
    return bcrypt.checkpw(password, hsh_password)
