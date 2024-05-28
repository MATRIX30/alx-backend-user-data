#!/usr/bin/env python3
"""
contains sql user model
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

# creating an instance of declarative base
# declarative base enable sqlalchemy to create
# tables from classes automatically
Base = declarative_base()


class User(Base):
    """Main user class"""

    __tablename__ = "users"  # name of table in db
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
