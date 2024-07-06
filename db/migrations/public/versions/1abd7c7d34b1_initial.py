""" initial

Revision ID: 1abd7c7d34b1
Revises: 
Create Date: 2024-07-06 17:45:04.426949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1abd7c7d34b1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('product_id', sa.UUID),
        sa.Column('type', sa.String),
        sa.Column('name', sa.String),
        sa.PrimaryKeyConstraint('product_id', name='products__pk'),
    )


def downgrade() -> None:
    op.drop_table('products')
