from .command import Command
from logging import getLogger

import typing as t


T = t.TypeVar("T")
logger = getLogger("bettercli")

@t.overload
def pos_option(name: 'str', type: 'type[T]', *, default: 'T' = None, length: 'int' = 1): ...

@t.overload
def pos_option(name: 'str', type: 'list[t.Optional[type]]' = None, *, default: 'list[t.Optional[t.Any]]' = None): ...

def pos_option(name, type=None, *, default=None, length=1):
    def decorator(cmd:'Command'):
        logger.debug(f"OPTIONS: {name=} {type=} {default=} {length=}")
        cmd.add_positional_option(name, type, default=default, length=length)
        return cmd
    return decorator



@t.overload 
def kw_option(name: 'str', type: 'type[T]', *keys: str, default: 'T' = None, length: 'int' = 1, max_occurrences: 'int' = 1): ...

@t.overload
def kw_option(name: 'str', type: 'list[t.Optional[type]]' = None, *keys: str, default: 'list[t.Optional[t.Any]]' = None, max_occurrences: 'int' = 1): ...

def kw_option(name, type=None, *keys, default=None, length=1, max_occurrences=1):
    def decorator(cmd:'Command'):
        logger.debug("KW ARG")
        cmd.add_keyword_option(name, type, default, *keys, length=length, max_occurrences=max_occurrences)
        return cmd
    return decorator
