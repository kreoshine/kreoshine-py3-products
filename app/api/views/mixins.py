"""
Mixins that may be used for views
"""
from typing import Mapping

from aiohttp.web_exceptions import HTTPBadRequest, HTTPInternalServerError

from app.api.validation.validator import CustomValidator


class ValidationMixin:
    """ Provides useful methods for validation and normalization """

    @staticmethod
    def get_validated_query_params(
            query_params: Mapping,
            validation_schema: dict,
    ) -> dict[str, str | list]:
        """ Method to get validated query params

        Note: method is not support multiple keys to combine list
            e.g. '?fields=name,fields=type' -> '{fields: [name, type]}'
            use '?fields=name,type' instead

        Args:
            query_params: raw query params mapping
            validation_schema: schema to be used for query params validation

        Returns:
            parsed params as a native python object
        Raises:
            HTTPBadRequest: when incorrect query params provided:
                - due to duplicated keys in query params (not allowed)
                - due to validation error
        """
        if len(set(query_params.keys())) < len(query_params.keys()):
            raise HTTPBadRequest(reason="duplicate param keys not allowed")
        validator = CustomValidator(validation_schema)
        validator.validate(dict(query_params))
        if validator.errors:
            raise HTTPBadRequest(reason=f"validation error: {validator.errors}")
        return validator.document

    @staticmethod
    def get_normalized_data(data: list | dict, structure_for_normalization: dict) -> dict:
        """ Method to normalize data for
            - serialization support

        Args:
            data: data to normalize
            structure_for_normalization: structure to be used for schema completing to normalize data;
                note: enriching is necessary to define data as dictionary (according to Cerberus abilities)
        Returns:
            normalized data as native python object (dictionary)
        Raises:
            HTTPInternalServerError: when error occurred on serialization
        """
        normalization_schema = {'data': structure_for_normalization}
        enrich_data = {'data': data}
        validator = CustomValidator(normalization_schema)
        validator.validate(enrich_data)
        if validator.errors:
            raise HTTPInternalServerError(reason=f'error on serialization ({validator.errors})')
        return validator.document['data']
