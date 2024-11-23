"""
Module with special print methods
"""


class _BC:
    """ Class with background colors """
    CORRAL = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    SIMPLE = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def brew_step(msg: str):
    """ print message as step """
    print(f"--> {_BC.CYAN}{msg}{_BC.SIMPLE}")


def echo_header(msg: str):
    """ print message as header """
    print(f"{_BC.CORRAL}{msg}{_BC.SIMPLE}")


def echo_note(msg: str):
    """ print message for note """
    print(f"{_BC.UNDERLINE}{msg}{_BC.SIMPLE}")


def echo_fail(msg: str):
    """ print message as fail """
    print(f"{_BC.RED}{msg}{_BC.SIMPLE}")


def echo_success(msg: str):
    """ print message as success """
    print(f"{_BC.GREEN}{msg}{_BC.SIMPLE}")


def echo_skip(msg: str):
    """ print message as success """
    print(f"{_BC.GREEN}{msg}{_BC.SIMPLE}")
