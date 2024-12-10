"""
Module with validator logic
"""
from uuid import UUID

from cerberus import Validator


class CustomValidator(Validator):
    """ Custom validator that is used for validation and normalization """

    def _validate_unique_items(self, constraint, field, value):
        """ Validation rule to check
         that list doesn't contain duplicate elements

        Example:
            my_list: {
                'type': 'list',
                'unique_items': True | False
            }
        """
        if constraint is False:
            return
        if constraint is not True:
            self._error(field, f"unexpected value '{constraint}' for constraint")
            return
        if not value:
            return
        if not isinstance(value, list):
            self._error(field, f"value '{value}' must be of 'list' type")
            return
        unique_elements = set(value)
        if len(unique_elements) != len(value):
            self._error(field, 'Duplicate items not allowed')

    @staticmethod
    def _normalize_coerce_to_list_from_comma_separated_string(value: str):
        """ Normalization rule (prefix `_normalize_coerce_`)
        that converts string separated by comma to list
        """
        return [item for item in value.split(',')]

    def _normalize_coerce_strip(self, value: str):
        """ Normalization rule (prefix `_normalize_coerce_`)
        that remove leading and trailing whitespaces
        """
        if not isinstance(value, str):
            self._error(f"'strip' rule require 'str' type for '{value}' value")
            return

        return value.strip()

    @staticmethod
    def _normalize_coerce_to_string_from_uuid(value: UUID):
        """ Normalization rule (prefix `_normalize_coerce_`)
        that converts UUID to string
        """
        return str(value)
