"""
Database utilities
"""
from alembic.config import Config as AlembicConfig

from settings import DB_PATH, ALEMBIC_INI_PATH


def get_alembic_config(section_name, database_url: str):
    alembic_config = AlembicConfig(
        file_=ALEMBIC_INI_PATH,
        ini_section=section_name,
    )

    # apply absolute path to alembic directory
    alembic_location = alembic_config.get_main_option('script_location')
    alembic_config.set_main_option('script_location', str(DB_PATH / alembic_location))

    # bound database URL
    alembic_config.set_main_option('sqlalchemy.url', database_url)

    return alembic_config
