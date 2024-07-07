"""
Model of 'products' table
"""
from sqlalchemy import (
    Table, Column,
    UUID, String,
)

from db import metadata

Product = Table(
    'products',
    metadata,
    Column('product_id', UUID, primary_key=True),
    Column('name', String),
    Column('type', String),
)
