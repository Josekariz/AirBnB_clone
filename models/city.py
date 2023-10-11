#!/usr/bin/python3
"""Def the City class."""
from models.base_model import BaseModel


class City(BaseModel):
    """Rep a city.

    Attributes:
        state_id (str): state id.
        name (str): name of the city.
    """

    state_id = ""
    name = ""
