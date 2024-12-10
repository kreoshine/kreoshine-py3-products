"""
Mixins that may be used for views
"""
from typing import Mapping

from aiohttp.web_exceptions import HTTPBadRequest, HTTPInternalServerError

from app.api.validation.validator import CustomValidator


class ValidatorMixin:
    """ Provides useful methods for validation and normalization """

    @staticmethod
    def get_normalized_query_params(
            query_params: Mapping,
            validation_schema: dict,
    ) -> dict[str, str | list]:
        """ Method to get parsed query params

        Note: method is not support multiple keys to combine list
            e.g. '?fields=name,fields=type' -> '{fields: [name, type]}'
            use '?fields=name,type' instead

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
            raise HTTPBadRequest(reason=f"validation error: {validator.errors}")
        return validator.document

    @staticmethod
    def get_normalized_data(data: dict, normalization_schema: dict) -> dict:
        """ Method to normalize data for response

        Args:
            data: data to normalize
            normalization_schema: schema to be used for data normalization

        Returns:
            normalize data a native python object (dictionary)
        Raises:
            HTTPInternalServerError: when error occurred on serialization
        """
        validator = CustomValidator(normalization_schema)
        validator.validate(data)
        if validator.errors:
            raise HTTPInternalServerError(reason=f'error on serialization ({validator.errors})')
        return validator.document
