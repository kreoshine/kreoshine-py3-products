"""
Service API
"""
import logging

from aiohttp.web import View
from aiohttp.web_response import Response, json_response

from app import const
from app.api.helpers import QueryParamsParser
from db.dao import DAOProducts

logger = logging.getLogger('service')


class ProductsView(View):
    """ API for '/products' route """

    @property
    def _dao_products(self) -> DAOProducts:
        return self.request.app['dao_products']

    @property
    def _query_params_parser(self) -> QueryParamsParser:
        return QueryParamsParser(query_params=self.request.rel_url.query)

    async def get(self) -> Response:
        """ Handler for GET '/products'

        Retrieves products from database

        Supported query params:
            - fields
        """
        query_params = self._query_params_parser.get_query_params()
        # todo: validate query params

        products_info = await self._dao_products.get_list_by_filter(
            requested_fields=query_params[const.api.query.FIELDS],
        )
        return json_response(products_info)
