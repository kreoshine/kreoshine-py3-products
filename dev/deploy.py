"""
Development deploy running module
"""
import subprocess

from alembic.command import upgrade
from sqlalchemy import create_engine, inspect, make_url
from sqlalchemy_utils import database_exists, create_database

from dev import BC
from settings import PROJECT_ROOT_PATH
from tests.plugins.database import get_database_url, create_enrich_alembic_config


def up_docker_compose_with_detach_option():
    """ Performs command to start containers (described in 'compose' file) in the background """
    command_to_execute = f"docker compose -f {PROJECT_ROOT_PATH / 'dev/docker-compose.yml'} up --detach"
    print(f"--> {BC.OKCYAN}{command_to_execute}{BC.ENDC}")
    command_stat = subprocess.run(
        command_to_execute, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    if command_stat.returncode:
        print(f"{BC.FAIL}{command_stat.stdout}{BC.ENDC}")
    else:
        print(f"{BC.OKGREEN}{command_stat.stdout}{BC.ENDC}")


def perform_dev_deploy():
    """ Performs deploy for development:
        - creation database if necessary
        - migration to HEAD for all schemas
    """
    print(f"--> {BC.OKCYAN}CREATE DATABASE{BC.ENDC}")
    database_url = get_database_url()  # note: avoid to use make_url here to keep the password in clear text
    database_name = make_url(database_url).database
    if database_exists(database_url):
        print(f"{BC.OKBLUE}database '{database_name}' already exists{BC.ENDC}")
    else:
        create_database(database_url)
        print(f"{BC.OKGREEN}database '{database_name}' created{BC.ENDC}")

    schemas_to_upgrade = ['public']  # note: section names in alembic.ini
    print(f"--> {BC.OKCYAN}database migrations{BC.ENDC}")
    for schema in schemas_to_upgrade:
        print(f"{BC.HEADER}perform migration for '{schema}' schema{BC.ENDC}")
        alembic_config = create_enrich_alembic_config(database_url, section_name=schema)
        upgrade(alembic_config, 'head')

    engine = create_engine(database_url)
    with engine.connect() as conn:
        inspector = inspect(conn)
        assert 'products' in inspector.get_table_names()
