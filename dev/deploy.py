"""
Development deploy running module
"""
import os.path
import shutil
import subprocess

from alembic.command import upgrade
from sqlalchemy import create_engine, inspect, make_url
from sqlalchemy_utils import database_exists, create_database

from app.__main__ import start_service
from dev.utils.echo import *
from settings import config, PROJECT_ROOT_PATH
from tests.plugins.database import get_database_url, create_enrich_alembic_config

TMP_DIR = PROJECT_ROOT_PATH / 'tmp'


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
        assert 'product' in inspector.get_table_names()


def __configure_environment():
    echo_header("prepare necessary environment for dynaconf")

    environment_file_path = PROJECT_ROOT_PATH / "settings/config/.env"
    environment_mode_line = "export KREOSHINE_ENV=DEVELOPMENT"
    try:
        need_to_add_environment_mode_line = True
        with open(environment_file_path, 'r') as fp:
            for line in fp.readlines():
                if line == environment_mode_line:
                    need_to_add_environment_mode_line = False
                    echo_skip("necessary environment already prepared")
        is_environment_file_exists = True
    except FileNotFoundError:
        is_environment_file_exists = False
        need_to_add_environment_mode_line = True

    if need_to_add_environment_mode_line:
        mode = 'a+' if is_environment_file_exists else 'w'
        with open(environment_file_path, mode) as fp:
            fp.write(environment_mode_line)
            echo_success("environment is successfully prepared")


def __create_tmp_dir():
    echo_header("prepare temporary directory")
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)
        echo_success(f"successfully created directory ({TMP_DIR})")
    else:
        print(f"directory already exists ({TMP_DIR})")


def __use_tmp_dir_for_logs(need_to_clear_logs: bool = True):
    """ Updates file paths for logging

    Args:
        need_to_clear_logs: boolean reflecting need to remove all logs, by default True

    Side effects:
        - clear log files before applying
        - new path definition for logging (PROJECT_DIR/tmp/logs/)
     """
    echo_header("provide logging in temporary directory")
    assert config.deploy.mode == 'development'

    log_dir = TMP_DIR / 'logs'

    if os.path.exists(log_dir) and need_to_clear_logs:
        echo_note(f"remove directory for logs: {log_dir}")
        shutil.rmtree(log_dir)

    if not os.path.exists(log_dir):
        echo_success(f"create directory for logs: {log_dir}")
        os.mkdir(log_dir)

    handlers = config.logging['handlers']
    for handler_name, handler_data in handlers.items():
        target_log_file_path = log_dir / f'{handler_name}.log'
        print(f"set '{target_log_file_path}' file for '{handler_name}' handler")
        handler_data['filename'] = str(target_log_file_path)


def _perform_dev_start():
    """ Performs service start for development
    
    Side effects:
        - creation necessary environment
        - creation temporary directory if necessary
        - configuring logging in 'tmp' directory
    """
    brew_step("development service start")
    __configure_environment()
    __create_tmp_dir()
    __use_tmp_dir_for_logs()
    echo_header("start service application")
    start_service()


def perform_dev_deploy():
    _up_docker_environment()
    _initialize_database()
    _perform_dev_start()
