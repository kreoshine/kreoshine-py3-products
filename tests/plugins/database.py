"""
Database plugin
"""
from random import choice
from string import ascii_uppercase, digits
from types import NoneType
from typing import Protocol, List

import pytest
from alembic.config import Config as AlembicConfig, Config
from alembic.script import ScriptDirectory
from alembic.script.revision import Revision
from sqlalchemy_utils import create_database, drop_database

from settings import config, PROJECT_ROOT_PATH

DB_PATH = PROJECT_ROOT_PATH / 'db/'


def get_database_url(enrich_dbname_with_suffix: bool = False) -> str:
    """ Prepares test database URL from config

    Args:
        enrich_dbname_with_suffix: boolean reflecting need to add 'test' suffix for database name, by default False
    Returns:
        database URL as string
    """
    database_name = config.db.database_name
    if enrich_dbname_with_suffix:
        database_name += f"-test-{choice(ascii_uppercase + digits)}"
    return '{driver_name}://{username}:{password}@{host}:{port}/{database}'.format(
        driver_name=f"{config.db.driver}+{config.db.dialect}",
        username=config.db.username,
        password=config.db.password,
        host=config.db.host,
        port=config.db.port,
        database=database_name,
    )


@pytest.fixture(scope='session')
def _test_database_url() -> str:
    """ Fixture provides database URL for testing

    Note: random string adds for the database name
    """
    return get_database_url(enrich_dbname_with_suffix=True)


@pytest.fixture(scope='session')
def _created_test_database(_test_database_url: str) -> None:
    """ Fixture creates test database

    Args:
        _test_database_url: database URL for creation
    Teardown effect:
        - dropping created database
    """
    print(f"create db: {_test_database_url}")
    create_database(_test_database_url)
    yield
    print(f"drop db: {_test_database_url}")
    drop_database(_test_database_url)


def create_enrich_alembic_config(database_url: str, section_name: str) -> AlembicConfig:
    """ Creates config for alembic and enrich it with passed args

    Args:
        database_url: database URL to apply for config
        section_name: name of the section for selecting migration scripts` location to be expanded to full path
    """
    alembic_config = AlembicConfig(
        file_=DB_PATH / 'alembic.ini',
        ini_section=section_name,
    )

    # apply absolute path to migration scripts
    alembic_location = alembic_config.get_main_option('script_location')
    alembic_config.set_main_option('script_location', str(DB_PATH / alembic_location))

    # bound database URL
    alembic_config.set_main_option('sqlalchemy.url', database_url)

    return alembic_config


class FixtureToCreateAlembicConfig(Protocol):
    """ Type of 'create alembic config' fixture

    Call params:
        section_name: section of alembic.ini to be used for creation
    """
    def __call__(self, section_name: str) -> AlembicConfig: ...


@pytest.fixture(scope='module')
def create_test_alembic_config(
        _created_test_database: NoneType,
        _test_database_url: str,
) -> FixtureToCreateAlembicConfig:
    """ Fixture prepares function which creates 'enrich' config of Alembic

    Args:
        _created_test_database: created database fixture
        _test_database_url: database URL fixture,
            note: URL must be string to provide password as is

    Returns:
        function for getting alembic config
    """
    def _create_test_alembic_config(section_name):
        return create_enrich_alembic_config(
            database_url=_test_database_url,
            section_name=section_name,
        )
    return _create_test_alembic_config


def get_revisions(alembic_config: Config) -> List[Revision]:
    """ Gets revisions specified in config of Alembic

    Args:
        alembic_config: Alembic config to be used for retrieving
    Returns:
        list of ordered revisions (from first to last)
    """
    # get directory object with Alembic migrations
    revisions_dir = ScriptDirectory.from_config(alembic_config)

    # get & sort migrations
    revisions = list(revisions_dir.walk_revisions('base', 'heads'))
    revisions.reverse()
    return revisions
