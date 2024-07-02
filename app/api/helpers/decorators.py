"""
Decorators for API
"""
import inspect
import logging
from datetime import datetime
from functools import wraps
from traceback import format_exc
from typing import Callable


def handler_decorated(
        logger: logging.Logger,
) -> Callable:
    """
    Decorator for wrapping json-rpc methods with logging
    Args:
        logger: logger to use

    Returns:
        decorated function
    """

    def wrap_method(fn):
        @wraps(fn)
        async def wrapped(*args, **kw):
            start_time = datetime.now()
            request = args[0].request

            try:
                logger.debug('[%s] start handling', fn.__name__)
                ret = await fn(*args, **kw)
                logger.debug(
                    "[%s] result time: %d ms",
                    fn.__name__,
                    round((datetime.now() - start_time).total_seconds() * 1000)
                )
                return ret
            except Exception:  # pylint: disable = broad-exception
                logger.exception(
                    '[%s] exception \n%s',
                    fn.__name__,
                    format_exc()
                )
                raise

        return wrapped

    return wrap_method


def view_decorated(decorator: Callable) -> Callable:
    """
    Decorates all rpc_* methods of a class with decorator

    Args:
        decorator: decorator to be applied to all rpc_ methods

    Returns:
        class decorator

    """
    allowed_rest_methods = {'get', 'post', 'patch', 'delete', 'put'}

    def class_decorator(cls):
        for name, method in inspect.getmembers(cls):
            if name in allowed_rest_methods:
                setattr(cls, name, decorator(method))
        return cls

    return class_decorator
