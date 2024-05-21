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
        if path is None:
            return True
        if not path.endswith("/"):
            path = path + "/"
        if excluded_paths is None or excluded_paths == []:
            return True
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """
        returns authorized headers
        """
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar("User"):
        """
        returns current user
        """
