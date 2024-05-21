#!/usr/bin/env python3
"""Module to handle basic authentication
"""


from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar
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

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str,
            ) -> Tuple[str, str]:
        """Extracts user credentials from a base64-decoded authorization
        header that uses the Basic authentication flow.
        """
        if type(decoded_base64_authorization_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            field_match = re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip(),
            )
            if field_match is not None:
                user = field_match.group('user')
                password = field_match.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Retrieves a user based on the user's authentication credentials.
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the user from a request.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
