import logging
import typing as t

T = t.TypeVar("T")
logger = logging.getLogger("bettercli")

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
