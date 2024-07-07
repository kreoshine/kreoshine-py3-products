"""
TODO
"""
from sqlalchemy import create_engine, Inspector

from dev.scripts.db import create_dev_database, upgrade_migrations_to_head
from dev.scripts.docker import up_docker_compose_with_detach_option
from dev.utils.base_utils import get_tmp_dir_path
from tests.utils.db import get_dev_database_url


def perform_dev_deploy():
    """ todo """
    up_docker_compose_with_detach_option()
    database_url = get_dev_database_url(dbname_suffix=False)
    print(f"database URL: {database_url}")

    create_dev_database(database_url)
    upgrade_migrations_to_head(
        database_url,
        dev_alembic_location=get_tmp_dir_path(),
    )

    engine = create_engine(database_url)
    with engine.connect() as conn:
        inspector = Inspector(conn)
        assert 'products' in inspector.get_table_names()


if __name__ == '__main__':
    perform_dev_deploy()
