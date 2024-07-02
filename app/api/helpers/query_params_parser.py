"""
Module with helper for parsing query string
"""
import logging
from typing import Dict, Union, Iterable

from aiohttp.web_exceptions import HTTPBadRequest
from cerberus import Validator
from multidict import MultiDict

logger = logging.getLogger('service')


class QueryParamsParser:
    """ Class is responsible for query string parsing

    Note: instance of current class must be created for each request
    """

    def __init__(self, query_params: MultiDict):
        self._raw_query_params = query_params

    def get_query_params(
            self,
            validation_schema: dict,
            list_values: Iterable[str] | None,
    ) -> Dict[str, Union[str, list]]:
        """ Method to get parsed query params

        Args:
            validation_schema: schema to be used for query params validation
            list_values: keys of values that should be parsed as list

        Returns:
            parsed params as a native python object
        Raises:
            HTTPBadRequest: when incorrect query params provided
        """
        query_params = {}
        if not self._raw_query_params:
            return query_params

        for key, value in self._raw_query_params.items():
            if key in list_values:
                if ',' in value:
                    value = value.split(',')
                else:
                    value = [value]
            if key not in query_params:
                query_params[key] = value
            else:
                raise HTTPBadRequest(reason="non-unique query parameters are not supported")

        validator = Validator(validation_schema)
        validator.validate(query_params)
        if validator.errors:
            raise HTTPBadRequest(reason=validator.errors)
        logger.debug("Normalized query params: %s", validator.document)
        return query_params
