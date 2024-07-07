"""
Database utils
"""
from sqlalchemy import URL

from settings import config


def get_database_url() -> URL:
    """ Forms database URL by config """
    return URL.create(
        drivername=config.db.driver,
        username=config.db.username,
        password=config.db.password,
        host=config.db.host,
        port=config.db.port,
        database=config.db.database_name,
    )
