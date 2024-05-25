#!/usr/bin/env python3
"""Module to handle basic authentication
"""


from api.v1.auth.auth import Auth


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
