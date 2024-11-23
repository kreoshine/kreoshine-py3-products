"""
Module with helper for parsing query string
"""
from typing import Dict, Union, Iterable, Mapping

from aiohttp.web_exceptions import HTTPBadRequest
from cerberus import Validator


def parse_query_params(
        raw_query_params: Mapping,
        validation_schema: dict,
        params_with_list_values: Iterable[str] | None = tuple(),
) -> Dict[str, Union[str, list]]:
    """ Method to get parsed query params

    Args:
        raw_query_params: raw query params mapping
        validation_schema: schema to be used for query params validation
        params_with_list_values: keys of values that should be parsed as list, optional
            e.g. fields=name,type => {'fields': ['name', 'type']}

    Returns:
        parsed params as a native python object
    Raises:
        HTTPBadRequest: when incorrect query params provided
    """
    parsed_query_params = {}
    if not raw_query_params:
        return parsed_query_params

    for key, value in raw_query_params.items():  # type: str, str
        if key in parsed_query_params:
            raise HTTPBadRequest(reason="non-unique query parameters are not supported")
        if key in params_with_list_values:
            if ',' in value:
                normalized_value = [item.strip() for item in value.split(',')]
            else:
                normalized_value = [value.strip()]
        else:
            normalized_value = value.strip()
        parsed_query_params[key] = normalized_value

    validator = Validator(validation_schema)
    validator.validate(parsed_query_params)
    if validator.errors:
        raise HTTPBadRequest(reason=validator.errors)
    return validator.document
