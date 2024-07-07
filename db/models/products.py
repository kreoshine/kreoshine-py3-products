"""
Model of 'products' table
"""
from sqlalchemy import (
    Table,
    Column, PrimaryKeyConstraint,
    UUID, String,
)

from db import metadata

Products = Table(
    'products',
    metadata,
    Column('product_id', UUID),
    Column('name', String),
    Column('type', String),
    PrimaryKeyConstraint('product_id', name='products__product_id__pkey'),
)
