"""
Mixins that may be used for views
"""
from typing import Mapping

from aiohttp.web_exceptions import HTTPBadRequest

from app.api.validation.validator import CustomValidator


class ValidatorMixin:
    """ Provides useful methods for validation and normalization """

    @staticmethod
    def get_normalized_query_params(
            query_params: Mapping,
            validation_schema: dict,
    ) -> dict[str, str | list]:
        """ Method to get parsed query params

        Args:
            query_params: raw query params mapping
            validation_schema: schema to be used for query params validation

        Returns:
            parsed params as a native python object
        Raises:
            HTTPBadRequest: when incorrect query params provided
        """
        validator = CustomValidator(validation_schema)
        validator.validate(dict(query_params))
        if validator.errors:
            raise HTTPBadRequest(reason=validator.errors)
        return validator.document
