"""
Database utils
"""

from settings import config


def get_database_url() -> str:
    """ Forms database URL by config """
    return '{driver}://{username}:{password}@{host}:{port}/{database}'.format(
        driver=config.db.driver,
        username=config.db.username,
        password=config.db.password,
        host=config.db.host,
        port=config.db.port,
        database=config.db.database_name,
    )
