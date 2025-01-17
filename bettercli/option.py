import typing as t
from logging import getLogger
from .utils import List, ListEnd, Length
from .exceptions import InvalidType, InvalidLength, TooManyOccurrences


logger = getLogger("bettercli")

@t.runtime_checkable
class Option[**P, R](t.Protocol):
    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> 'None': ...

    def validate(self, *args: P.args, **kwargs: P.kwargs) -> 'R': ...


class ValidType[**P, R](t.Protocol):
    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> 'None': ...

T = t.TypeVar("T", bound=ValidType)



class Keyword_option(t.Generic[T]):
    def __init__(self, name:'str', type:'list[type[T]]'=[None], *keys, default:'list[T]'=[None], length=1, max_occurrences=1):
        logger.debug(f"Keyword_option.__init__: {name=} {type=} {keys=} {default=} {length=} {max_occurrences=}")
        for k in keys:
            if not k.startswith("-"):
                raise ValueError("Keyword options must start with `-`")
        self.keys = keys
        self.type = List(type)
        self.name = name
        self.length = length
        self.max_occurrences = max_occurrences
        self.occurrences = 0
        self.default = default if isinstance(default, list) else [default]
        self.default += [None for _ in range(length - len(self.default))]

    def validate(self, options: 'list[t.Any]') -> 't.Union[InvalidLength, InvalidType, TooManyOccurrences, list[T]]':
        logger.debug(f"Keyword_option.validate({self.name}): {options=}")
        name = options.pop(0)
        self.occurrences += 1
        if self.occurrences > self.max_occurrences:
            return TooManyOccurrences(self, name, self.max_occurrences, self.occurrences)
    

        if len(options) < self.length:
            logger.debug(f"Keyword_option.validate({self.name}): Length is less than length: {len(options)=} < {self.length=}")
            logger.debug(f"Keyword_option.validate({self.name}): Applying defaults: {self.default=}")
            for default in self.default[len(options):]:
                logger.debug(f"Keyword_option.validate({self.name}): Adding default: {default=}")
                if default is None:
                    logger.debug("Default is None")
                    return InvalidLength(self, options, self.length)
            
                options.append(default)

        logger.debug(f"Keyword_option.validate({self.name}): Finished applying defaults: {options=}")
        for key, option, type in zip(range(len(options)), options, self.type):
            if type is None:
                continue

            try:
                logger.debug(f"Keyword_option.validate({self.name}): Trying to cast {option=} to {type=}")
                options[key] = type(option)
            except ValueError:
                return InvalidType(self, option, type)

        if len(options) == 1:
            logger.debug(f"Keyword_option.validate({self.name}): Returning {options[0]=}")
            return options[0]
        logger.debug(f"Keyword_option.validate({self.name}): Returning {options=}")
        return options
    
    def __repr__(self) -> 'str':
        return f"Option(name={self.name}, type={self.type}, default={self.default})"

class Positional_option(t.Generic[T]):
    def __init__(self, name:'str', type:'type[T]'=None, *, default=None, length=1):
        logger.debug(f"Positional_option.__init__: {name=} {type=} {default=} {length=}")
        if length < 1:
            raise ValueError("Positional options must have a length of at least 1")
        self.type = type
        self.default = default
        self.name = name
        self.max_length = length
        self.extended = length > 1
        self.length = 0

    @property
    def has_default(self) -> 'bool':
        logger.debug("Positional_option.has_default")
        return self.default is not None


    def validate(self, option: 'str', cur_option: 'list[str]'=[]) -> 'tuple[t.Union[InvalidType, InvalidLength, t.Literal[True]], bool]':
        self.length += 1
        if self.length > self.max_length:
            return InvalidLength(self, cur_option, self.max_length), True
        try:
            if self.type is None:
                cur_option.append(option)
                return True, len(cur_option)+1 >= self.max_length
            
            cur_option.append(self.type(option)) # type: ignore
            return True, len(cur_option) >= self.max_length
        except ValueError:
            return InvalidType(self, option, self.type), self.length >= self.max_length
        
    def __repr__(self) -> 'str':
        return f"Positional_option(name={self.name}, type={self.type}, max_length={self.max_length}, default={self.default})"