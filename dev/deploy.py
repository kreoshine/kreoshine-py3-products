"""
Development deploy running module
"""
import subprocess

from alembic.command import upgrade
from sqlalchemy import create_engine, inspect, make_url
from sqlalchemy_utils import database_exists, create_database

from app.__main__ import start_service
from dev.utils.echo import *
from dev.utils.logging import use_tmp_dir_for_logs
from settings import PROJECT_ROOT_PATH
from tests.plugins.database import get_database_url, create_enrich_alembic_config


def _up_docker_environment():
    """ Performs command to start containers (described in 'compose' file) """
    brew_step("Up docker environment")
    command_to_execute = f"docker compose -f {PROJECT_ROOT_PATH / 'dev/docker-compose.yml'} up --detach"
    echo_header(command_to_execute)
    command_stat = subprocess.run(
        command_to_execute, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    if command_stat.returncode:
        echo_fail(command_stat.stdout)
    else:
        echo_success(command_stat.stdout)


def _initialize_database():
    """ Prepares database for application with next steps:
        - creation database if necessary
        - migration to HEAD for all schemas
    """
    brew_step("create database")
    database_url = get_database_url()  # note: avoid to use make_url here to keep the password in clear text
    database_name = make_url(database_url).database
    if database_exists(database_url):
        echo_skip(f"database '{database_name}' already exists")
    else:
        create_database(database_url)
        echo_success(f"database '{database_name}' created")

    schemas_to_upgrade = ['public']  # note: section names in alembic.ini
    brew_step("database migrations")
    for schema in schemas_to_upgrade:
        echo_header(f"perform migration for '{schema}' schema")
        alembic_config = create_enrich_alembic_config(database_url, section_name=schema)
        upgrade(alembic_config, 'head')

    engine = create_engine(database_url)
    with engine.connect() as conn:
        inspector = inspect(conn)
        assert 'products' in inspector.get_table_names()


def _perform_dev_start():
    """ Performs service start for development
    
    Side effects:
        - configuring logging in 'tmp' directory
    """
    use_tmp_dir_for_logs()
    start_service()
