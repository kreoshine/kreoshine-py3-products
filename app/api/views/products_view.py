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
    RESPONSE_JSON__NORMALIZATION_STRUCTURE__PRODUCTS,
)
from app.api.views.mixins import ValidationMixin
from db.dao import ProductDAO

logger = logging.getLogger('service')


@rest_view_decorated(logger)
class ProductsView(View, CorsViewMixin, ValidationMixin):
    """ REST API for '/api/products' route """

    @property
    def _product_dao(self) -> ProductDAO:
        """ Product Data Access Object """
        return self.request.app['product_dao']

    async def get(self) -> Response:
        """ Handler for GET '/products'

        Retrieves products info from database

        Supported query params:
            - fields — specifies fields to be requested, e.g. `?fields=id,name,type`

        Data in response:
            ``` json
            [
                {
                    'id': 'some-product-uuid4',
                    'type': 'some-type',
                    'name': 'some localized product name'
                },
                {...},
            ]
            ```
        """
        query_params = self.get_validated_query_params(
            query_params=self.request.rel_url.query,
            validation_schema=QUERY_PARAMS_VALIDATION_SCHEMA__GET_PRODUCTS,
        )
        logger.debug("normalized query params: %s", query_params)
        products_db_data = await self._product_dao.query(
            query_fields=query_params.get(const.query.FIELDS),
        )
        return json_response(
            data=self.get_normalized_data(
                products_db_data,
                structure_for_normalization=RESPONSE_JSON__NORMALIZATION_STRUCTURE__PRODUCTS
            )
        )
