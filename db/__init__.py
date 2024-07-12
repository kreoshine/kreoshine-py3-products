"""
Package with database logic
"""
from sqlalchemy import MetaData, URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from settings import config

metadata = MetaData()


class BaseModel(DeclarativeBase):
    """ Base class for models"""
    metadata = metadata


def get_database_url() -> URL:
    """ Forms database URL by config """
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


def get_async_engine() -> AsyncEngine:
    """ Creates async engine based on database URL

    Returns:
        engine, see more at sqlalchemy.create_engine
    """
    return create_async_engine(
        url=get_database_url()
    )
