"""
Service API
"""
import logging

from aiohttp.web import View
from aiohttp.web_response import Response, json_response
from aiohttp_cors import CorsViewMixin

from app.api import const
from app.api.helpers.decorators import rest_view_decorated, rest_handler_decorated
from app.api.helpers.query_params_parsing import parse_query_params
from app.api.helpers.serialization import custom_dumps
from app.api.validation.schemas.products_validation_schemas import PRODUCTS_QUERY_PARAMS__GET__SCHEMA
from db.dao import ProductsDAO

logger = logging.getLogger('service')


@rest_view_decorated(rest_handler_decorated(logger))
class ProductsView(View, CorsViewMixin):
    """ API for '/api/products' route """

    @property
    def _products_dao(self) -> ProductsDAO:
        return self.request.app['products_dao']

    # @validated(PRODUCTS_QUERY_PARAMS__GET__SCHEMA)
    async def get(self) -> Response:
        """ Handler for GET '/products'

        Retrieves products info from database

        Supported query params:
            - field — specifies fields to be requested
        """
        query_params = parse_query_params(
            raw_query_params=self.request.rel_url.query,
            params_with_list_values=[const.query.keys.FIELDS],
            validation_schema=PRODUCTS_QUERY_PARAMS__GET__SCHEMA,
        )
        logger.debug("Normalized query params: %s", query_params)
        products_db_data = await self._products_dao.query(
            query_fields=query_params.get(const.query.FIELDS),
        )
        return json_response(
            products_db_data,
            dumps=custom_dumps,
        )
