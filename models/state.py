#!/usr/bin/python3
"""Defines the State class."""
from models.base_model import BaseModel


class State(BaseModel):
    """Rep a state.

    Attributes:
        name (str): Name of the state.
    """

    name = ""
