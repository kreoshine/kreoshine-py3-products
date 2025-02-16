"""
Application initialization
"""
import logging
import logging.config
import sys

from aiohttp import web
from aiohttp_cors import setup, ResourceOptions
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.api.views import ProductsView
from db import get_database_url
from db.dao import ProductDAO

from settings import config

logger = logging.getLogger('service')


def __configure_logging() -> None:
    """ Configures logging config for an application

    Side effects:
        - apply except-hook for unexpected errors
    """
    logging.config.dictConfig(config=config.logging)

    def _handle_exception(exc_type, exc_value, exc_traceback) -> None:
        """ Handler for uncaught exceptions """
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical("Uncaught exception!", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = _handle_exception


async def __init_db_components(app: web.Application):
    engine_url = get_database_url()
    logger.debug("create engine (URL: %s)", engine_url)
    engine = create_async_engine(url=engine_url)
    app['engine'] = engine

    product_dao = ProductDAO(engine)
    logger.debug("product DAO created")
    app['product_dao'] = product_dao


async def _start_service_components(app: web.Application):
    logger.info("start service components")
    await __init_db_components(app)


async def _stop_service_components(app: web.Application):
    logger.info("stop service components")
    engine = app['engine']  # type: AsyncEngine
    logger.debug("close engine (URL: %s)", engine.url)
    await engine.dispose()


def create_app() -> web.Application:
    """ Creates instance of web application """
    __configure_logging()
    logger.info("deploy mode: %s", config.deploy.mode)

    app = web.Application(
        logger=logger,
        client_max_size=config.app.client_max_size_bytes,
    )
    app.on_startup.append(_start_service_components)
    app.on_shutdown.append(_stop_service_components)

    routes_definition = (
        web.view(config.app.endpoints.products, ProductsView),
    )

    app.add_routes(routes_definition)

    cors = setup(app, defaults={
        "*": ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    for route in list(app.router.routes()):
        cors.add(route)

    logger.debug(f"registered resources: {[resource.get_info().get('path') for resource in app.router.resources()]}")

    logger.info("instance of web-application successfully created")
    return app
