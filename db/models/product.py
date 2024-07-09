"""
Model of 'products' table
"""
from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from db import metadata


# declarative base class
class Base(DeclarativeBase):
    """ Base class for models"""
    pass
    # metadata = metadata


class Product(Base):
    """
    Model for product
    """
    __tablename__ = 'products'

    product_id: Mapped[str] = mapped_column(UUID, primary_key=True)
    name: Mapped[str]
    type: Mapped[str]
