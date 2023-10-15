#!/usr/bin/python3
"""Def Amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Rep an amenity.

    Attributes:
        name (str): name of amenity.
    """

    name = ""
