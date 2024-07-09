"""
todo
"""
import logging
from typing import List, Optional, Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import load_only, InstrumentedAttribute

from db import const
from db.models import Product

logger = logging.getLogger('service')

PRODUCTS_DATA = [
    {
        'type': 'default',
        'name': 'KreoShine',
        'images_data': [
            {
                'url': '/static/images/logo.svg',
                'title': 'KreoShine',
            },
        ],
        'descriptions_content': [
            'Lorem the best',
            'agdsh328',
        ],
    }
]


class DAOProducts:
    """ Data access object for products """

    def __init__(
            self,
            engine: AsyncEngine,
    ):
        self._engine = engine

    @property
    def async_session(self) -> AsyncSession:
        return async_sessionmaker(self._engine)()

    @property
    def _filed_to_column_mapper(self) -> dict[str, InstrumentedAttribute]:
        return {
            const.product.NAME: Product.name,
            const.product.TYPE: Product.type,
        }

    async def get_list_by_filter(
            self,
            # filters: Iterable[dict] = (),
            # order: Iterable[dict] = (),
            # limit: Optional[int] = None,
            # offset: Optional[int] = None,
            requested_fields: Optional[List[str]] = None,
    ) -> List[dict]:
        """ todo """
        stmt = select(Product)

        # options = []
        if requested_fields:
            querycolumns = [self._filed_to_column_mapper[column] for column in requested_fields]
            # options.append(load_only(*columns_to_load))
            # query_attributes = [Product.type, Product.name]
            stmt = select(*querycolumns)
        else:
            stmt = select(Product)

        # if options:
        #     stmt = stmt.options(*options)
        #
        # data = []
        # async with self.async_session as session:
        #     result = await session.execute(stmt)
        #     logger.debug(result)
        #     # result = result.fetchall()
        #     for item in result.scalars():
        #         item = {field: getattr(item, field) for field in requested_fields}
        #         logger.debug(item)
        #         data.append(item)
        # return data
        # return_value = [row.type for row in result]
        # for row in result:
        #     item = {key: value for key, value in zip(requested_fields, row)}
        #     return_value.append(item)
        # logger.debug(return_value)

        async with self._engine.connect() as conn:
            result = await conn.execute(stmt)
            result = result.fetchall()
        return_value = []
        for row in result:
            item = {key: value for key, value in zip(requested_fields, row)}
            return_value.append(item)
        logger.debug("result: %s", return_value)
        return return_value

        # async with self._async_session() as session:
        #     result = (await session.execute(stmt)).all()
        # return [dict(item) for item in result]
        #
        # result = []
        # for product_data in PRODUCTS_DATA:
        #     product_info = {}
        #     for product_field, value in product_data.items():
        #         if requested_fields is not None and product_field in requested_fields:
        #             product_info[product_field] = value
        #     result.append(product_info)
        # return result
