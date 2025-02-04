"""
Database API implemented via 'Data Access Object' pattern over ORM
"""
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import QueryableAttribute

from db import metadata
from db.models import Product


class ProductDAO:
    """ Data Access Object of product

    Provides async methods for interacting with the database
    """

    def __init__(
            self,
            engine: AsyncEngine,
    ):
        self._engine = engine

    @property
    def _names_to_columns_map(self) -> dict[str, QueryableAttribute]:
        return {
            column_name: column for column_name, column
            in zip(
                metadata.tables[Product.__tablename__].columns.keys(),
                metadata.tables[Product.__tablename__].columns
            )
        }

    async def query(
            self,
            query_fields: Optional[List[str]] = None,
    ) -> List[dict]:
        """ Executes a database query over ORM to retrieve entities

        Note: query is executed without a transaction

        Args:
            query_fields: names of columns to query, optional;
                note: if not passed all columns will be retrieved
        Returns:
            list with queried entities as dicts
        """
        if query_fields:
            query_columns = [self._names_to_columns_map[fields_name] for fields_name in query_fields]
            stmt = select(*query_columns)
        else:
            query_fields = self._names_to_columns_map.keys()
            stmt = select(Product)

        async with self._engine.connect() as conn:
            result = await conn.execute(stmt)
        return [
            {field: value for field, value in zip(query_fields, row)}
            for row in result.fetchall()
        ]
