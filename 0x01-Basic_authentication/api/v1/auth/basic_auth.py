#!/usr/bin/env python3
"""Basic authentication module for the API.
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class.
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization header
        for a Basic Authentication.
        """
        if type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)'
            field_match = re.fullmatch(pattern, authorization_header.strip())
            if field_match is not None:
                return field_match.group('token')
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str,
            ) -> str:
        """Decodes a base64-encoded authorization header.
        """
        if type(base64_authorization_header) == str:
            try:
                res = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                return res.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
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
        """Retrieves the User instance for a request.

        Args:
            request (:obj:`Request`, optional): The request object. Defaults
            to None.

        Returns:
            User: The User instance based on the request.
        """
        # Get the authorization header from the request
        auth_header = self.authorization_header(request)
        # Extract the Base64 encoded string from the authorization header
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        # Decode the Base64 encoded string
        dec_header = self.decode_base64_authorization_header(b64_auth_header)
        # Extract the user email and password from the decoded Base64 string
        user_email, user_pwd = self.extract_user_credentials(dec_header)
        # Return the User instance based on the user email and password
        return self.user_object_from_credentials(user_email, user_pwd)
