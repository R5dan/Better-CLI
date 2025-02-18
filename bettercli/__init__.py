from logging import INFO
from .decorators import pos_option, kw_option
from .logger import TogglableDebugLogger
from .cli import CLI
from . import cl


logger = TogglableDebugLogger("bettercli", INFO)


__all__ = ["CLI", "pos_option", "kw_option"]