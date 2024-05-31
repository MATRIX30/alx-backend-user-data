#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User
from typing import TypeVar


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.
        Args:
            email: The email address of the user.
            hashed_password: The hashed password of the user.

        Returns:
            A User object representing the newly added user.
        """
        session = self._session
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            session.add(new_user)
            session.commit()
        except Exception as e:
            print("Error adding new user: {}".format(e))
            session.rollback()
            return
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """method to find user based in kwargs
        Args:
             kwargs{dic}: list of keyword arguments
        Return:
             User: whose attributes match the kwargs
                    or None otherwise with exception raised
        """
        # found_user = self._session.query(User).filter_by(
        #    email=kwargs.get('email')).first()
        try:
            found_user = self._session.query(User).filter_by(**kwargs).one()
            return found_user
        except NoResultFound:
            raise NoResultFound("No Item Found")
        except InvalidRequestError:
            raise InvalidRequestError("search term mismatch")

    def update_user(self, user_id: int, **kwargs) -> None:
        """method to update user information with user_id
        Args:
             user_id(int): user id of the user to update
        Returns:
             None
        """
        user = self.find_user_by(id=user_id)
        user_attrib = user.__dict__.copy()
        del user_attrib['_sa_instance_state']
        for k, v in kwargs.items():
            if k not in user_attrib:
                raise ValueError("attribute doesn't match")
            setattr(user, k, v)
        return None
