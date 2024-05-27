#!/usr/bin/python3
""" City Module for HBNB project """


from models.base_model import Base, BaseModel
from models.state import State
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """
    The city class, contains state ID and name
    """

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'cities'

        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship("Place", backref="cities",
                              cascade="all, delete-orphan")
        state = relationship("State", back_populates="cities")
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """Initialize State"""
        super().__init__(*args, **kwargs)


# State.cities = relationship("City", order_by=City.id, back_populates='state')
