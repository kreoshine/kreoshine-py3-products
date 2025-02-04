"""
Module with database ORM models
"""

from sqlalchemy.orm import Mapped

from db import BaseModel


class Product(BaseModel):
    """
    Model for product
    """
    __tablename__ = 'product'

    name: Mapped[str]
    type: Mapped[str]
