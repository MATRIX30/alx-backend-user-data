#!/usr/bin/env python3
"""
Module to handle authentication
"""


from flask import request
from typing import List, TypeVar


class Auth:
    """
    class to handle API authentications
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        method to return required authentication
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        returns authorized headers
        """
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """
        returns current user
        """
