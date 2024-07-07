"""
Database utilities
"""
from random import choice
from string import hexdigits

from settings import config


def get_dev_database_url(dbname_suffix: bool = True) -> str:
    """ Prepares test database URL from config

    Args:
        dbname_suffix: boolean reflecting need to add random string suffix for database name

    Returns:
        database URL as string
    """
    database_name = config.db.database_name
    if dbname_suffix:
        database_name += f"-{''.join(choice(hexdigits) for i in range(5))}"
    return '{driver_name}://{username}:{password}@{host}:{port}/{database}'.format(
        driver_name=f"{config.db.driver}+{config.db.dialect}",
        username=config.db.username,
        password=config.db.password,
        host=config.db.host,
        port=config.db.port,
        database=database_name,
    )
