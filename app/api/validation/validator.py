"""
Module with validator logic
"""
from uuid import UUID

from cerberus import Validator


class CustomValidator(Validator):
    """ Custom validator that is used for validation and normalization """

    @staticmethod
    def _normalize_coerce_to_list_from_comma_separated_string(value: str):
        """ Normalization rule (prefix `_normalize_coerce_`)
        that converts string separated by comma to list
        """
        return [item.strip() for item in value.split(',')]

    @staticmethod
    def _normalize_coerce_to_string_from_uuid(value: UUID):
        """ Normalization rule (prefix `_normalize_coerce_`)
        that converts UUID to string
        """
        return str(value)
