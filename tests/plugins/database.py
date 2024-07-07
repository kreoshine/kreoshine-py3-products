"""
Database plugin
"""
from typing import Callable

import pytest
from alembic.config import Config as AlembicConfig
from sqlalchemy_utils import create_database, drop_database

from settings import DB_PATH, ALEMBIC_INI_PATH
from tests.utils.db import get_dev_database_url


@pytest.fixture(scope='session')
def _test_database_url() -> str:
    """ Fixture. Prepares database URL for testing

    Note: random string adds for the database name
    """
    return get_dev_database_url()


@pytest.fixture(scope='session')
def created_database(_test_database_url) -> None:
    """ Fixture. Prepares database creation

    Teardown effect:
        - dropping created database
    """
    print(f"create db: {_test_database_url}")
    create_database(_test_database_url)
    yield
    print(f"drop db: {_test_database_url}")
    drop_database(_test_database_url)


@pytest.fixture(scope='module')
def get_alembic_config(created_database, _test_database_url) -> Callable:
    """ Parameterized fixture.
    Result function gets 'alembic' config for specified section of alembic.ini with bounding to database URL

    Args:
        created_database: created database fixture
        _test_database_url: database URL fixture

    Real params:
        section_name: section of alembic.ini

    Returns:
        function for getting alembic config
    """
    def _get_alembic_config(section_name):
        alembic_config = AlembicConfig(
            file_=ALEMBIC_INI_PATH,
            ini_section=section_name,
        )

        # apply absolute path to alembic directory
        alembic_location = alembic_config.get_main_option('script_location')
        alembic_config.set_main_option('script_location', str(DB_PATH / alembic_location))

        # bound database URL
        alembic_config.set_main_option('sqlalchemy.url', _test_database_url)

        return alembic_config
    return _get_alembic_config
