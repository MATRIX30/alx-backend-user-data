#!/usr/bin/env python3
"""Module to handle basic authentication
"""


from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    class to handle basic authentication
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extracts the base64 part of request header authorization string"""

        # request_data =request.headers["Authorization"]
        if authorization_header is None:
            return None
        if not (type(authorization_header) == str):
            return None
        if not (authorization_header.startswith("Basic ")):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """method to decode base64 encoding"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            decoded_base64_header = base64.b64decode(
                base64_authorization_header)
            decoded_str_msg = decoded_base64_header.decode("utf-8")
            return decoded_str_msg
        except Exception:
            return None
