import logging
from bettercli.option import Option
from bettercli.utils import Length

logger = logging.getLogger("bettercli")

class BetterCLIException(Exception):
    """Base class for all exceptions raised by BetterCLI"""

class InvalidOption(BetterCLIException):
    """Base class for invalid option"""
    def __init__(self, option:'Option', op):
        logger.debug(f"InvalidOption: {option=} {op=}")
        self.option = option
        self.op = op

class InvalidType(InvalidOption):
    """Raised when an option is not of the correct type"""
    def __init__(self, option:'Option', op, expected:'Length'):
        logger.debug(f"InvalidType: {option=} {op=} {expected=}")
        super().__init__(option, op)
        self.expected = expected

class InvalidLength(InvalidOption):
    """Raised when an option is not the correct length"""
    def __init__(self, option:'Option', op, expected):
        logger.debug(f"InvalidLength: {option=} {op=}")
        super().__init__(option, op)
        self.expected = expected