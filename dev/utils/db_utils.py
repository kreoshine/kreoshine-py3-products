"""
Database utilities
"""
from alembic.command import upgrade
from psycopg.errors import DuplicateDatabase
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_utils import create_database

from tests.plugins.database import create_enrich_alembic_config, get_revisions


def upgrade_migrations_to_head(database_url: str, schema: str):
    """ TODO """
    alembic_config = create_enrich_alembic_config(database_url, section_name=schema)
    revisions = get_revisions(alembic_config)
    for revision in revisions:
        upgrade(alembic_config, revision.revision)


def create_dev_database(database_url: str) -> None:
    """ Creates database for development

    Note: database will be created if not already exists

    Args:
        database_url: todo
    Raises:
        ProgrammingError: todo
    """
    try:
        create_database(database_url)
    except ProgrammingError as err:
        if DuplicateDatabase.__name__ in str(err):
            print(err)
        else:
            raise
