""" Development utils to customize logging """
import os
import shutil

from settings import config, PROJECT_ROOT_PATH

TMP_DIR = PROJECT_ROOT_PATH / 'tmp'


def use_tmp_dir_for_logs(need_to_clear_logs: bool = True):
    """ Updates file paths for logging

    Args:
        need_to_clear_logs: boolean reflecting need to remove all logs, by default True

    Side effects:
        - clear log files before applying
        - new path definition for logging (PROJECT_DIR/tmp/logs/)
     """
    assert config.deploy.mode == 'development'

    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)

    log_dir = TMP_DIR / 'logs'

    if os.path.exists(log_dir) and need_to_clear_logs:
        shutil.rmtree(log_dir)

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    handlers = config.logging['handlers']
    for handler_name, handler_data in handlers.items():
        handler_data['filename'] = str(log_dir / f'{handler_name}.log')
