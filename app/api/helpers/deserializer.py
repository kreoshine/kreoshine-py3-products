"""
TODO
"""
import json
import uuid


class Deserializer:
    """
    JSON deserializer with special logic:
        - converts UUID data types to strings
    """

    @staticmethod
    def _callback_on_error(data_value):
        if isinstance(data_value, uuid.UUID):
            return str(data_value)
        raise TypeError(f"Unsupported deserialization for '{data_value}' (type: {type(data_value)})")

    def __call__(self, obj):
        return json.dumps(obj, default=self._callback_on_error)
