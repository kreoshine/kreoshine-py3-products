"""
Module with stairway-testing
"""
from typing import List

from alembic.command import upgrade, downgrade
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.script.revision import Revision


def get_revisions(alembic_config: Config) -> List[Revision]:
    """ Gets revisions for alembic config

    Args:
        alembic_config: alembic config to be used for retrieving
    Returns:
        list of ordered revisions (from first to last)
    """
    # get directory object with Alembic migrations
    revisions_dir = ScriptDirectory.from_config(alembic_config)

    # get & sort migrations
    revisions = list(revisions_dir.walk_revisions('base', 'heads'))
    revisions.reverse()
    return revisions


def tests_db_migrations__stairway(get_alembic_config):
    """
    Performs stairway test for all migrations
    """
    alembic_config = get_alembic_config(section_name='public')
    revisions = get_revisions(alembic_config)
    for revision in revisions:
        upgrade(alembic_config, revision.revision)

        # note: -1 when down_revision is None (first migration)
        downgrade(alembic_config, revision.down_revision or '-1')
        upgrade(alembic_config, revision.revision)
