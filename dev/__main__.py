"""
TODO
"""
from dev.scripts.db import create_dev_database
from dev.scripts.docker import up_docker_compose_with_detach_option


def perform_dev_deploy():
    """ todo """
    up_docker_compose_with_detach_option()
    create_dev_database()


if __name__ == '__main__':
    perform_dev_deploy()
