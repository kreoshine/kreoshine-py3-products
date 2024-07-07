"""
Base development utilities
"""
import os
from pathlib import Path

from settings import PROJECT_ROOT_PATH


def get_tmp_dir_path() -> Path:
    """ todo """
    tmp_dir_path = PROJECT_ROOT_PATH / 'tmp'
    if not os.path.exists(tmp_dir_path):
        os.mkdir(tmp_dir_path)
    return tmp_dir_path
