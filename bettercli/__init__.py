from logging import getLogger, INFO
from .decorators import CLI, pos_option, kw_option
from .logger import TogglableDebugLogger

logger = TogglableDebugLogger("bettercli", INFO)
logger.enable_debug()

__all__ = ["CLI", "pos_option", "kw_option"]