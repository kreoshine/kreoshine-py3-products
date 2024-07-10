"""
TODO
"""
import subprocess
from time import sleep

from sqlalchemy import create_engine, inspect

from dev import BC
from dev.utils.db_utils import create_dev_database, upgrade_migrations_to_head
from settings import PROJECT_ROOT_PATH
from tests.plugins.database import get_database_url


def up_docker_compose_with_detach_option():
    """ Performs command to start containers (described in 'compose' file) in the background """
    command_to_execute = f"docker compose -f {PROJECT_ROOT_PATH / 'dev/docker-compose.yml'} up --detach"
    print(f"--> {BC.OKCYAN}{command_to_execute}{BC.ENDC}")
    command_stat = subprocess.run(command_to_execute, shell=True)
    command_stat.check_returncode()
    print(f"Result code: {command_stat.returncode}")


def provide_pause(seconds: int) -> None:
    """ Provides pause

    Args:
        seconds: seconds to wait
    """
    while seconds != 0:
        print(f"waiting (left {seconds} seconds)")
        seconds -= 1
        sleep(1)


def perform_dev_deploy():
    """ todo """
    print(f"{BC.HEADER}START CREATION DEV ENVIRONMENT{BC.ENDC}")
    up_docker_compose_with_detach_option()
    provide_pause(seconds=3)

    database_url = get_database_url()
    create_dev_database(database_url)
    schemas_to_upgrade = ['public']  # note: section names in alembic.ini
    for schema in schemas_to_upgrade:
        upgrade_migrations_to_head(database_url, schema)

    engine = create_engine(database_url)
    with engine.connect() as conn:
        inspector = inspect(conn)
        assert 'products' in inspector.get_table_names()


if __name__ == '__main__':
    perform_dev_deploy()
