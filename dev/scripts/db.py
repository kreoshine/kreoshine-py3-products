"""
Database scripts
"""
import subprocess

from psycopg.errors import DuplicateDatabase
from sqlalchemy import Inspector, create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_utils import create_database

from dev.utils.base_utils import get_tmp_dir_path
from settings import ALEMBIC_INI_PATH, DB_PATH
from tests.utils.db import get_dev_database_url


def _create_database_if_not_exist(database_url):
    try:
        create_database(database_url)
    except ProgrammingError as err:
        if DuplicateDatabase.__name__ in str(err):
            print(err)
        else:
            raise


def _perform_migration(database_url):
    tmp_dir_path = get_tmp_dir_path()
    tmp_alembic_ini_path = tmp_dir_path / 'alembic.ini'
    public_script_location_path = DB_PATH / 'migrations/public'
    subprocess.call(
        f"cp {ALEMBIC_INI_PATH} {tmp_alembic_ini_path}",
        shell=True,
    )
    command_to_execute = str(
        'sed -i '
        '-e "s|sqlalchemy.url.*|sqlalchemy.url = {DATABASE_URL}|" '
        '-e "s|script_location = migrations/public|script_location = {PUBLIC_SCRIPT_LOCATION_PATH}|" '
        '{TMP_ALEMBIC_INI_PATH}').format(
        DATABASE_URL=database_url,
        TMP_ALEMBIC_INI_PATH=tmp_alembic_ini_path,
        PUBLIC_SCRIPT_LOCATION_PATH=public_script_location_path,
    )
    subprocess.call(
        command_to_execute,
        shell=True,
    )
    subprocess.call(
        f"alembic -c {tmp_alembic_ini_path} -n public upgrade head",
        shell=True,
    )


def create_dev_database() -> None:
    """ Creates database """
    database_url = get_dev_database_url(dbname_suffix=False)
    print(f"database URL: {database_url}")

    _create_database_if_not_exist(database_url)
    _perform_migration(database_url)

    engine = create_engine(database_url)
    with engine.connect() as conn:
        inspector = Inspector(conn)
        assert 'products' in inspector.get_table_names()
