import logging
import typing as t
import inspect

if t.TYPE_CHECKING:
    from .command import Command
    from .option import Option
    from .utils import Length

logger = logging.getLogger("bettercli")

class BetterCLIException(Exception):
    """Base class for all exceptions raised by BetterCLI"""
    def __init__(self):
        loc = inspect.currentframe().f_back.f_back
        self.loc = loc.f_code.co_filename, loc.f_lineno

    def to_cli(self) -> 'str':
        raise NotImplementedError("`to_cli` must be implemented by subclasses")

class InvalidOption(BetterCLIException):
    """Base class for invalid option"""
    def __init__(self, option:'Option', op, expected):
        super().__init__()
        logger.debug(f"InvalidOption: {option=} {op=}")
        self.option = option
        self.op = op
        self.expected = expected

    def to_cli(self):
        return f"""
BetterCLI Exception
-------------------
{self.__class__.__name__}: {self}
{self.expected=} {self.op=} {self.option=}
Location: {self.loc}
"""
        

class InvalidCommand(BetterCLIException):
    """Raised when an option is not the correct length"""
    def __init__(self, command:'Command', op):
        super().__init__()
        logger.debug(f"InvalidCommand: {command=} {op=}")
        self.command = command
        self.op = op

    def to_cli(self):
        return f"""
BetterCLI Exception
-------------------
{self.__class__.__name__}: {self}
{self.command=} {self.op=}
Location: {self.loc}
"""

class InvalidType(InvalidOption):
    """Raised when an option is not of the correct type"""
    def __init__(self, option:'Option', op, expected:'Length'):
        logger.debug(f"InvalidType: {option=} {op=} {expected=}")
        super().__init__(option, op, expected)

class InvalidLength(InvalidOption):
    """Raised when an option is not the correct length"""
    def __init__(self, option:'Option', op, expected):
        logger.debug(f"InvalidLength: {option=} {op=}")
        super().__init__(option, op, expected)

class TooManyOccurrences(InvalidOption):
    """Raised when an option is not the correct length"""
    def __init__(self, option:'Option', op, expected, occurrences):
        logger.debug(f"TooManyOccurrences: {option=} {op=}")
        super().__init__(option, op, expected)
        self.occurrences = occurrences

    def to_cli(self):
        return f"""
BetterCLI Exception
-------------------
{self.__class__.__name__}: {self}
{self.option=} {self.op=} {self.expected=} {self.occurrences=}
Location: {self.loc}
"""