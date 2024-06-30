"""
Application initialization
"""
import logging
import logging.config
import sys

from aiohttp import web

from app.api.views import ProductsView
from db.dao import DAOProducts

try:
    from dev.utils import log_utils
except ImportError:
    log_utils = None

from settings import config

logger = logging.getLogger('service')


def __configure_logging() -> None:
    """ Configures logging

    Side effects:
        - (dev) updates log paths for 'development' deploy mode
        - apply except-hook for unexpected errors
    """
    if config.deploy.mode == 'development':
        log_utils.use_tmp_dir_for_logs()

    logging.config.dictConfig(config=config.logging)

    def _handle_exception(exc_type, exc_value, exc_traceback) -> None:
        """ Handler for uncaught exceptions """
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical("Uncaught exception!", exc_info=(exc_type, exc_value, exc_traceback))

    logger.info("Deploy mode: %s", config.deploy.mode)
    sys.excepthook = _handle_exception


async def __init_dao(app: web.Application):
    dao_products = DAOProducts()
    logger.debug("DAO for products created")
    app['dao_products'] = dao_products


def create_app() -> web.Application:
    """ Creates instance of web application """
    __configure_logging()

    app = web.Application(
        logger=logger,
        client_max_size=config.app.client_max_size_bytes,
    )
    app.on_startup.append(__init_dao)

    routes_definition = (
        web.view(config.app.endpoints.products, ProductsView),
    )

    app.add_routes(routes_definition)

    logger.debug(f"registered resources: {[resource.get_info().get('path') for resource in app.router.resources()]}")

    logger.info("Instance of web-application successfully created")
    return app
