"""
Service running module
"""
from aiohttp import web

from app import create_app
from settings import config


def start_service():
    """ Entry point to  application """
    web.run_app(
        app=create_app(),
        host=config.app['host'],
        port=config.app['port'],
        access_log_format=config.app['access_log_format']
    )


if __name__ == '__main__':
    start_service()
