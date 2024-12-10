"""
Service API
"""
import logging

from aiohttp.web import View
from aiohttp.web_response import Response, json_response
from aiohttp_cors import CorsViewMixin

from app.api import const
from app.api.helpers.decorators import rest_view_decorated
from app.api.validation.schemas import (
    QUERY_PARAMS_VALIDATION_SCHEMA__GET_PRODUCTS,
    NORMALIZATION_SCHEMA__PRODUCT,
)
from app.api.views.mixins import ValidationMixin
from db.dao import ProductsDAO

logger = logging.getLogger('service')


@rest_view_decorated(logger)
class ProductsView(View, CorsViewMixin, ValidationMixin):
    """ REST API for '/api/products' route """

    @property
    def _products_dao(self) -> ProductsDAO:
        return self.request.app['products_dao']

    async def get(self) -> Response:
        """ Handler for GET '/products'

        Retrieves products info from database

        Supported query params:
            - fields — specifies fields to be requested
        """
        query_params = self.get_validated_query_params(
            query_params=self.request.rel_url.query,
            validation_schema=QUERY_PARAMS_VALIDATION_SCHEMA__GET_PRODUCTS,
        )
        logger.debug("Normalized query params: %s", query_params)
        products_db_data = await self._products_dao.query(
            query_fields=query_params.get(const.query.FIELDS),
        )
        return json_response(
            [
                self.get_normalized_data(
                    data=product,
                    normalization_schema=NORMALIZATION_SCHEMA__PRODUCT
                )
                for product in products_db_data
            ]
        )
