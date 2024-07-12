"""
Module with database ORM models
"""

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column

from db import BaseModel


class Product(BaseModel):
    """
    Model for product
    """
    __tablename__ = 'products'

    product_id: Mapped[str] = mapped_column(UUID, primary_key=True)
    name: Mapped[str]
    type: Mapped[str]
