"""
Module with helper for parsing query string
"""
from typing import Dict, Union

from aiohttp.web_exceptions import HTTPBadRequest
from multidict import MultiDict


class QueryParamsParser:
    """ Class is responsible for query string parsing

    Note: instance of current class must be created for each request
    """

    def __init__(self, query_params: MultiDict):
        self._raw_query_params = query_params

    def get_query_params(self) -> Dict[str, Union[str, list]]:
        """ Method to get parsed query params

        Returns:
            parsed params as a native python object
        """
        query_params = {}
        if not self._raw_query_params:
            return query_params

        for key, value in self._raw_query_params.items():
            if ',' in value:
                value = value.split(',')
            if key not in query_params:
                query_params[key] = value
            else:
                raise HTTPBadRequest(reason="non-unique query parameters are not supported")

        return query_params
