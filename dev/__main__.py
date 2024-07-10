"""
TODO
"""
import subprocess

from sqlalchemy import create_engine, Inspector

from dev.utils.db_utils import create_dev_database, upgrade_migrations_to_head
from settings import PROJECT_ROOT_PATH
from tests.plugins.database import get_database_url


def up_docker_compose_with_detach_option():
    """ Performs command to start containers (described in 'compose' file) in the background """
    command_to_execute = f"docker compose -f {PROJECT_ROOT_PATH / 'dev/docker-compose.yml'} up --detach"
    print(f"--> {command_to_execute}")
    subprocess.call(command_to_execute, shell=True)


def perform_dev_deploy():
    """ todo """
    up_docker_compose_with_detach_option()
    database_url = get_database_url()
    print(f"database URL: {database_url}")

    create_dev_database(database_url)
    schemas_to_upgrade = ['public']  # note: section names in alembic.ini
    for schema in schemas_to_upgrade:
        upgrade_migrations_to_head(database_url, schema)

    engine = create_engine(database_url)
    with engine.connect() as conn:
        inspector = Inspector(conn)
        assert 'products' in inspector.get_table_names()


if __name__ == '__main__':
    perform_dev_deploy()
