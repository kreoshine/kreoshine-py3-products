"""
Development deploy running module
"""
import subprocess

from sqlalchemy import create_engine, inspect

from dev import BC
from dev.utils.db_utils import create_dev_database, upgrade_to_head_migration
from settings import PROJECT_ROOT_PATH
from tests.plugins.database import get_database_url


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
    print(f"{BC.HEADER}START CREATION DEV ENVIRONMENT{BC.ENDC}")
    database_url = get_database_url()
    create_dev_database(database_url)
    schemas_to_upgrade = ['public']  # note: section names in alembic.ini
    for schema in schemas_to_upgrade:
        upgrade_to_head_migration(database_url, schema)

    engine = create_engine(database_url)
    with engine.connect() as conn:
        inspector = inspect(conn)
        assert 'products' in inspector.get_table_names()
