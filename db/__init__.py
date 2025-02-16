"""
Package with database logic
"""
from sqlalchemy import URL

from settings import config


def get_database_url() -> URL:
    """ Forms database URL by Dynaconf config """
    driver_name = config.db.driver
    if config.db.get('dialect') and config.db.dialect:
        driver_name += f'+{config.db.dialect}'
    return URL.create(
        drivername=driver_name,
        username=config.db.username,
        password=config.db.password,
        host=config.db.host,
        port=config.db.port,
        database=config.db.database_name,
    )
