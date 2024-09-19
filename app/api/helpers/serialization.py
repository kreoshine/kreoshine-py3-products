"""
TODO
"""
import json
import uuid


def _custom_encode_callback(data_value):
    if isinstance(data_value, uuid.UUID):
        return str(data_value)
    raise TypeError(f"Unsupported deserialization for '{data_value}' (type: {type(data_value)})")


def custom_dumps(obj):
    """ Callback TODO """
    return json.dumps(obj, default=_custom_encode_callback)
