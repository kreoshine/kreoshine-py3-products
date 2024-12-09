"""
Module with validator logic
"""
from cerberus import Validator


class CustomValidator(Validator):
    """ Custom validator that is used for validation and normalization """

    def _normalize_coerce_to_list_from_comma_separated_string(self, value: str):
        """ Normalization rule (prefix `_normalize_coerce_`)
        that converts string separated by comma to list
        """
        return [item.strip() for item in value.split(',')]
