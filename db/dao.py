"""
Database API implemented via 'Data Access Object' pattern over ORM
"""
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import QueryableAttribute

from db.models import Product


class ProductsDAO:
    """ Data Access Object of products

    Provides async methods for interacting with the database
    """

    def __init__(
            self,
            engine: AsyncEngine,
    ):
        self._engine = engine

    @property
    def _product_columns_mapper(self) -> dict[str, QueryableAttribute]:
        return {
            column_name: column for column_name, column
            in zip(
                Product.metadata.tables['products'].columns.keys(),
                Product.metadata.tables['products'].columns
            )
        }

    async def query(
            self,
            query_fields: Optional[List[str]] = None,
    ) -> List[dict]:
        """ todo """
        if query_fields:
            query_columns = [self._product_columns_mapper[column_name] for column_name in query_fields]
            stmt = select(*query_columns)
        else:
            query_fields = self._product_columns_mapper.keys()
            stmt = select(Product)

        async with self._engine.connect() as conn:
            result = await conn.execute(stmt)
        return [
            {field: value for field, value in zip(query_fields, row)}
            for row in result.fetchall()
        ]
