"""
Database utilities
"""
from alembic.command import upgrade
from sqlalchemy import make_url
from sqlalchemy_utils import create_database, database_exists

from dev import BC
from tests.plugins.database import create_enrich_alembic_config


def create_dev_database(database_url: str) -> None:
    """ Creates database if not exists for development

    Args:
        database_url: URL of the database to create
    """
    print(f"{BC.HEADER}create database{BC.ENDC}")
    print(f"database URL: {database_url}")
    if database_exists(database_url):
        print(f"{BC.WARNING}database {make_url(database_url).database} already exists{BC.ENDC}")
    else:
        create_database(database_url)
        print(f"{BC.BOLD}database created{BC.ENDC}")


def upgrade_to_head_migration(database_url: str, schema: str) -> None:
    """ Upgrades database schema to HEAD migration

    Args:
        database_url: database URL, note: string type — to make possible password usage
        schema: schema name to be upgraded
    """
    print(f"{BC.HEADER}perform migration for '{schema}' schema{BC.ENDC}")
    alembic_config = create_enrich_alembic_config(database_url, section_name=schema)
    upgrade(alembic_config, 'head')
