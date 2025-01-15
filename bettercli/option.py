import typing as t
from logging import getLogger
from .utils import List, ListEnd, Length
from .exceptions import InvalidType, InvalidLength

T = t.TypeVar("T")
logger = getLogger("bettercli")


class Option(t.Generic[T]):
    @t.overload
    def __init__(self, name:'str', type:'t.Optional[type[T]]'=None, *, default:'t.Optional[T]'=None, length:'int'=2) -> None: ...
    # 0 or 1 input

    @t.overload
    def __init__(self, name:'str', type:'list[t.Optional[type]]'=[], *, default:'list[t.Optional[t.Any]]'=[], min_length:'int'=2, max_length:'int'=2) -> None: ...
    # Greater than 1 input

    def __init__(self, name:'str', type=None, *, default=None, length=None, min_length=None, max_length=None):
        logger.debug(f"Option.__init__: {name=} {type=} {default=} {length=} {min_length=} {max_length=}")
        if not (length or (min_length and max_length)):
            raise ValueError("Please specify either length or `max_length` and `min_length`")
        self.name = name
        self.default = List(default)
        self.type = List(type)
        self.length = Length(min_length, max_length, length)

    def validate(self, options:'list[str]') -> 't.Union[InvalidLength, InvalidType, list[T]]':
        logger.debug(f"Option.validate: {options=}")
        logger.debug(f"Option.validate: Validating length {len(options)} against min={self.length.min_length}, max={self.length.max_length}")
        if resp := not self.length.validate(len(options)):
            logger.debug(f"Option.validate: Invalid length {len(options)}, returning {not resp}")
            return InvalidLength(self, options)
        ret = []
        logger.debug(f"Option.validate: Validating types")
        for type_, option in zip(self.type, options):
            logger.debug(f"Option.validate: Validating {option} against {type_}")
            while isinstance(type_, ListEnd):
                type_ = next(type_.List)
                logger.debug(f"Option.validate: Got next type {type_}")
            
            if type_ is None:
                logger.debug(f"Option.validate: No type specified for {option}")
                ret.append(option)
                continue
            
            try:
                logger.debug(f"Option.validate: Converting {option} to {type_}")
                ret.append(type_(option))
                continue
            except:
                logger.debug(f"Option.validate: Failed to convert {option} to {type_}")
                return InvalidType(self, option, type_)
        
        if len(options) < self.length.min_length:
            logger.debug(f"Option.validate: Not enough options ({len(options)} < {self.length.min_length})")
            if len(self.default) <= self.length.min_length:
                return InvalidLength(self, options)
            else:
                logger.debug(f"Option.validate: Using defaults {self.default[len(options):]}")
                ret.extend(self.default[len(options):])
        
        if len(options) > self.length.max_length:
            logger.debug(f"Option.validate: Too many options ({len(options)} > {self.length.max_length})")
            return InvalidLength(self, options)
        
        logger.debug(f"Option.validate: Returning {ret}")
        return ret

class Keyword_option(Option[T]):
    def __init__(self, name:'str', type=None, *keys, default=None, length=None, min_length=None, max_length=None):
        logger.debug(f"Keyword_option.__init__: {name=} {type=} {keys=} {default=} {length=} {min_length=} {max_length=}")
        for k in keys:
            if not k.startswith("-"):
                raise ValueError("Keyword options must start with `-`")
        super().__init__(name, type, default=default, length=length, min_length=min_length, max_length=max_length)
        self.keys = keys

    def validate(self, options: 'list[str]') -> 't.Union[InvalidLength, InvalidType, bool]':
        logger.debug(f"Keyword_option.validate: {options=}")
        if options[0] not in self.keys:
            return False
        return super().validate(options[1:])

class Positional_option(Option[T]):
    def __init__(self, name:'str', type=None, *, default=None, length=None, min_length=None, max_length=None):
        logger.debug(f"Positional_option.__init__: {name=} {type=} {default=} {length=} {min_length=} {max_length=}")
        super().__init__(name, type, default=default, length=length, min_length=min_length, max_length=max_length)