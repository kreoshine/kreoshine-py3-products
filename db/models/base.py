"""
todo
"""
from sqlalchemy import MetaData, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = MetaData()


class BaseModel(DeclarativeBase):
    """ Base class for models """
    metadata = metadata
    id: Mapped[str] = mapped_column(UUID, primary_key=True)
