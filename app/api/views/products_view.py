"""
Service API
"""
import logging

from aiohttp.web import View
from aiohttp.web_response import Response, json_response

from app.api import const
from app.api.helpers import QueryParamsParser
from app.api.helpers.decorators import rest_view_decorated, rest_handler_decorated
from app.api.helpers.serialization import custom_dumps
from app.api.validation.schemas.products_validation_schema import PRODUCTS_QUERY_PARAMS__GET__SCHEMA
from db.dao import ProductsDAO

logger = logging.getLogger('service')


@rest_view_decorated(rest_handler_decorated(logger))
class ProductsView(View):
    """ API for '/products' route """

    @property
    def _products_dao(self) -> ProductsDAO:
        return self.request.app['products_dao']

    @property
    def _query_params_parser(self) -> QueryParamsParser:
        return QueryParamsParser(query_params=self.request.rel_url.query)

    async def get(self) -> Response:
        """ Handler for GET '/products'

        Retrieves products info from database

        Supported query params:
            - fields TODO
        """
        query_params = self._query_params_parser.get_query_params(
            list_values=[const.query.keys.FIELDS],
            validation_schema=PRODUCTS_QUERY_PARAMS__GET__SCHEMA,
        )
        products_db_data = await self._products_dao.query(
            query_fields=query_params.get(const.query.FIELDS),
        )
        return json_response(
            products_db_data,
            dumps=custom_dumps,
        )
