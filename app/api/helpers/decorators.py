"""
Decorators for API
"""
import inspect
import logging
from datetime import datetime
from functools import wraps
from traceback import format_exc
from typing import Callable, Union

from aiohttp.web_request import Request
from aiohttp.web_urldispatcher import View


def rest_handler_decorated(
        logger: logging.Logger,
) -> Callable:
    """ Decorator for wrapping REST handlers

    Args:
        logger: logger to use

    Returns:
        decorated async function
    """
    def _async_parametrized_deco(fn):
        @wraps(fn)
        async def _async_wrapper(handler_instance: Union[View, Request]):
            start_time = datetime.now()
            if isinstance(handler_instance, Request):
                request = handler_instance
            elif isinstance(handler_instance, View):
                request = handler_instance.request
            else:
                raise RuntimeError("Unexpected handler instance")

            call_action = "{} {}".format(request.method, request.rel_url.raw_path)
            try:
                logger.info('%s', call_action)
                ret = await fn(handler_instance)
                return ret
            except Exception:  # pylint: disable = broad-exception
                logger.exception('[%s] unexpected exception: \n%s', call_action, format_exc())
                raise
            finally:
                logger.debug(
                    "[%s] result time: %d ms", call_action, round((datetime.now() - start_time).total_seconds() * 1000)
                )
        return _async_wrapper
    return _async_parametrized_deco


def rest_view_decorated(decorator: Callable) -> Callable:
    """
    Decorates for REST methods of a view

    Args:
        decorator: decorator to be applied for all REST methods

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
