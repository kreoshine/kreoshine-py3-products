"""
Module with stairway-testing of migrations
"""

from alembic.command import upgrade, downgrade

from tests.plugins.database import FixtureToCreateAlembicConfig, get_revisions


def tests_db_migrations__stairway(create_test_alembic_config: FixtureToCreateAlembicConfig):
    """
    Performs stairway test for all migrations
    """
    # ARRANGE
    alembic_config = create_test_alembic_config(section_name='public')
    revisions = get_revisions(alembic_config)

    # ACT/ASSERT
    for revision in revisions:
        upgrade(alembic_config, revision.revision)

        # note: -1 when down_revision is None (first migration)
        downgrade(alembic_config, revision.down_revision or '-1')
        upgrade(alembic_config, revision.revision)
