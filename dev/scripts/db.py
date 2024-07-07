"""
Database scripts
"""
import subprocess
from pathlib import Path

from psycopg.errors import DuplicateDatabase
from sqlalchemy.exc import ProgrammingError
from sqlalchemy_utils import create_database

from settings import ALEMBIC_INI_PATH, DB_PATH


def create_dev_database(database_url: str) -> None:
    """ Creates database for development

    Note: database will be created if not already exists

    Args:
        database_url: 
    """
    try:
        create_database(database_url)
    except ProgrammingError as err:
        if DuplicateDatabase.__name__ in str(err):
            print(err)
        else:
            raise


def upgrade_migrations_to_head(database_url: str, dev_alembic_location: Path | str):
    """ Performs migration for database

    Note: original alembic.ini file will be copied and modified

    Args:
        database_url: 
        dev_alembic_location: directory to be used for creation alembic.ini file
    """
    dev_alembic_ini_path = dev_alembic_location / 'alembic.ini'
    public_script_location_path = DB_PATH / 'migrations/public'
    subprocess.call(
        f"cp {ALEMBIC_INI_PATH} {dev_alembic_ini_path}",
        shell=True,
    )
    update_dev_alembic_command = str(
        'sed -i '
        '-e "s|sqlalchemy.url.*|sqlalchemy.url = {DATABASE_URL}|" '
        '-e "s|script_location = migrations/public|script_location = {PUBLIC_SCRIPT_LOCATION_PATH}|" '
        '{TMP_ALEMBIC_INI_PATH}').format(
        DATABASE_URL=database_url,
        TMP_ALEMBIC_INI_PATH=dev_alembic_ini_path,
        PUBLIC_SCRIPT_LOCATION_PATH=public_script_location_path,
    )
    subprocess.call(
        update_dev_alembic_command,
        shell=True,
    )
    subprocess.call(
        f"alembic -c {dev_alembic_ini_path} -n public upgrade head",
        shell=True,
    )

