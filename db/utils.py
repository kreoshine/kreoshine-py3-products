"""
Database utils
"""

from settings import config


def get_database_url() -> str:
    """ Forms database URL by config """
    return '{driver}://{user}:{password}@{host}/{database}'.format(
        driver=config.db.driver,
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,
        database=config.db.database_name,
    )
