#!/usr/bin/env python3
"""Module to handle basic authentication
"""


from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """method to return users information from decoded base64"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if decoded_base64_authorization_header == '':
            return None, None
        login = decoded_base64_authorization_header.split(":")
        if len(login) != 2:
            return None, None
        email = login[0]
        password = login[1]
        if not(email and password):
            return None, None
        return email, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ returns the users instance based on email and password"""
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        try:
            search_user = User.search({"email": user_email})
        except Exception:
            return None
        if len(search_user) == 0:
            return None
        user = search_user[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self,
                     request=None) -> TypeVar('User'):
        """overloads Auth and retrieves User instance for a request"""
        if request is None:
            return None
        request_header = self.authorization_header(request)
        if request_header is None:
            return None
        base64header = self.extract_base64_authorization_header(request_header)
        decodedheader = self.decode_base64_authorization_header(base64header)
        user_info = self.extract_user_credentials(decodedheader)
        if user_info[0] is None or user_info[1] is None:
            return None
        email = user_info[0]
        password = user_info[1]
        user = self.user_object_from_credentials(email, password)
        if user is None:
            return None
        return user
