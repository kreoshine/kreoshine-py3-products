""" Development utils to customize logging """
import os
import shutil

from dev.utils.base_utils import get_tmp_dir_path
from settings import config


def use_tmp_dir_for_logs(need_to_clear_logs: bool = True):
    """ Updates file paths for logging

    Args:
        need_to_clear_logs: boolean reflecting need to remove all logs, by default True

    Side effects:
        - clear log files before applying
        - new path definition for logging (PROJECT_DIR/tmp/logs/)
     """
    assert config.deploy.mode == 'development'
    tmp_dir_path = get_tmp_dir_path()
    log_dir = tmp_dir_path / 'logs'

    if os.path.exists(log_dir) and need_to_clear_logs:
        shutil.rmtree(log_dir)

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    handlers = config.logging['handlers']
    for handler_name, handler_data in handlers.items():
        handler_data['filename'] = str(log_dir / f'{handler_name}.log')
