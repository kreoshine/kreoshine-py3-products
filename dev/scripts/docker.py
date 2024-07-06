"""
Docker scripts for development
"""
import subprocess
from settings import PROJECT_ROOT_PATH

DOCKER_COMPOSE_FILE_PATH = PROJECT_ROOT_PATH / 'dev/docker-compose.yml'


def up_docker_compose_with_detach_option():
    """ Performs command to start containers (described in 'compose' file) in the background """
    command_template_to_execute = "docker compose -f {DOCKER_COMPOSE_FILE_PATH} up --detach"
    subprocess.call(
        command_template_to_execute.format(DOCKER_COMPOSE_FILE_PATH=DOCKER_COMPOSE_FILE_PATH),
        shell=True,
    )
