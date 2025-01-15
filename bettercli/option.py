import typing as t
from logging import getLogger

T = t.TypeVar("T")
logger = getLogger("bettercli")

class InvalidOption:
    """Base class for invalid option"""
    def __init__(self, option:'Option', op):
        logger.debug(f"InvalidOption: {option=} {op=}")
        self.option = option
        self.op = op

class InvalidType(InvalidOption):
    """Raised when an option is not of the correct type"""
    def __init__(self, option:'Option', op, expected):
        logger.debug(f"InvalidType: {option=} {op=} {expected=}")
        super().__init__(option, op)
        self.expected = expected

class InvalidLength(InvalidOption):
    """Raised when an option is not the correct length"""
    def __init__(self, option:'Option', op):
        logger.debug(f"InvalidLength: {option=} {op=}")
        super().__init__(option, op)

class ListEnd:
    def __init__(self, List, list, no):
        logger.debug(f"ListEnd: {List=} {list=} {no=}")
        self.List:'List' = List
        self.list:'list' = list
        self.no:'int' = no

class List(t.Generic[T]):
    def __init__(self, item:'t.Union[T, t.Iterable[T]]'):
        logger.debug(f"List.__init__: {item=}")
        if isinstance(item, t.Iterable):
            self.list = list(item)
        else:
            self.list = [item]
        
    def __iter__(self) -> 't.Self':
        logger.debug("List.__iter__")
        self.i = -1
        self.r = -1
        return self
    
    def __next__(self) -> 't.Union[T, ListEnd]':
        logger.debug(f"List.__next__: {self.i=} {self.r=}")
        if len(self.list) == 1:
            return self.list[0]
        
        if len(self.list) == 0:
            raise StopIteration
        
        self.i += 1
        if len(self.list) == self.i+1:
            self.r += 1
            self.i = 0
            return ListEnd(self, self.list, self.r)
        return self.list[self.i]
    
    def __getattr__(self, name):
        logger.debug(f"List.__getattr__: {name=}")
        return getattr(self.list, name)
    
    def __getitem__(self, name):
        logger.debug(f"List.__getitem__: {name=}")
        return self.list[name]

    def __len__(self):
        logger.debug("List.__len__")
        return len(self.list)
    
class Length:
    MinMax, Len = True, False
    def __init__(self, min:'int|None'=None, max:'int|None'=None, len:'int|None'=None):
        logger.debug(f"Length.__init__: {min=} {max=} {len=}")
        self.min = min
        self.max = max
        self.len = len

        if not ((isinstance(min, int) and isinstance(max, int)) or isinstance(len, int)):
            raise ValueError("Please specify either `min` and `max` or `len`")

    def validate(self, length:'int') -> 'bool':
        logger.debug(f"Length.validate: {length=}")
        if isinstance(self.min, int) and isinstance(self.max, int):
            logger.debug(f"Length.validate: {length=} {self.min=} {self.max=}")
            return length >= self.min and length <= self.max
        elif isinstance(self.len, int):
            logger.debug(f"Length.validate: {length=} {self.len=}")
            return length == self.len
        else:
            raise ValueError("Please specify either `min` and `max` or `len`. Not both.")
    
    @property
    def type(self):
        logger.debug("Length.type")
        if self.min and self.max:
            return self.MinMax
        return self.Len
    
    @property
    def min_length(self) -> 'int':
        logger.debug("Length.min_length")
        return self.min or self.len # type: ignore
    
    @property
    def max_length(self) -> 'int':
        logger.debug("Length.max_length")
        return self.max or self.len # type: ignore

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