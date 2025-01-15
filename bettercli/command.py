import typing as t
import logging

from .option import Keyword_option, Positional_option, Option
from .exceptions import InvalidLength, InvalidType

T = t.TypeVar("T")
logger = logging.getLogger("bettercli")

@t.runtime_checkable
class Callback(t.Protocol):
    def __call__(self, **kwargs) -> None: ...

class Command:
    options:'dict[str, Option]' = {}
    pos_options:'dict[str, Positional_option]' = {}
    kw_options:'dict[str, Keyword_option]' = {}
    commands: 'list[Command]' = []
    types = [str, int, float]

    def __init__(self, name:'str', callback:'Callback'=lambda **kwargs: None) -> None:
        logger.debug(f"Command.__init__: {name=} {callback=}")
        self.name = name
        self._callback = callback
        self.options = {}
        self.pos_options = {}
        self.kw_options = {}
        self.commands = []

    @property
    def callback(self):
        logger.debug("Command.callback getter")
        return self._callback
    
    @callback.setter
    def callback(self, value):
        logger.debug(f"Command.callback setter: {value=}")
        self._callback = value

    @t.overload
    def add_subcommand(self, callback:'Callback', name:'str'=None, command:'Command'=None): ...

    @t.overload
    def add_subcommand(self, command:'Command'=None, name:'str'=None, callback:'Callback'=None): ...

    def add_subcommand(self, callback:'Callback'=lambda **kwargs: None, name:'str'=None, command:'Command'=None):
        if command is not None:
            self.commands.append(command)
        elif name is not None:
            self.commands.append(Command(name=name, callback=callback))
        else:
            raise ValueError("Must provide either a command or a name")
    
    def subcommand(self, name:'str'):
        def decorator(func):
            command = Command(name=name, callback=func)
            self.add_subcommand(command)
            return command
        return decorator


    def add_positional_option(self, name:'str', type_:'type[T]', default:'T', *, length:'int|None'=None, min_length:'int|None'=None, max_length:'int|None'=None):
        logger.debug(f"Command.add_positional_option: {name=} {type_=} {default=} {length=} {min_length=} {max_length=}")
        if name in self.options:
            raise ValueError(f"{name} already defined. {name} is a {type(self.options[name]).__name__} with type {self.options[name].type}")
        option = Positional_option(name, type_, default=default, length=length, min_length=min_length, max_length=max_length)
        self.pos_options[name] = option
        self.options[name] = option

    def add_keyword_option(self, name, _type, default, *kws, length:'int|None'=None, min_length:'int|None'=None, max_length:'int|None'=None):
        logger.debug(f"Command.add_keyword_option: {name=} {_type=} {default=} {kws=} {length=} {min_length=} {max_length=}")
        if name in self.options:
            raise ValueError(f"{name} already defined. {name} is a {type(self.options[name]).__name__} with type {self.options[name].type}")

        option = Keyword_option(name, _type, *kws, default=default, length=length, min_length=min_length, max_length=max_length)
        self.kw_options[name] = option
        self.options[name] = option

    @property
    def schema(self):
        logger.debug("Command.schema")
        return [self.name] + [option for option in self.options.keys()]
    
    def run(self, command:'list[str]'):
        logger.debug(f"Command.run: {command=}")
        if self.validate(command):
            options = {}
            logger.debug(f"Command.run: Validated command. Processing options: {self.options}")
            for name, option in self.options.items():
                logger.debug(f"Command.run: Validating option: {option.name}")
                op = option.validate(command[1:])
                if op is False:
                    logger.debug(f"Command.run: Option {name} validation returned False")
                    return
                elif isinstance(op, InvalidType):
                    logger.debug(
                        f"""
                        Invalid type for option {name}
                        Expected {op.expected}
                        Got {op.op}
                        """
                        )
                elif isinstance(op, InvalidLength):
                    logger.debug(f"Command.run: Invalid length for option {name}")
                    pass
                options[name] = op

            logger.debug(f"Command.run: Calling callback with options: {options}")
            self.callback(**options)

    def add_types(self, type):
        logger.debug(f"Command.add_types: {type=}")
        self.types.append(type)

        
        
    def validate(self, command:'list[str]'):
        logger.debug(f"Command.validate: {command=} {command[1:]=}")
        if command[0] != self.name:
            logger.debug(f"Command.validate: Command name mismatch. Expected {self.name}, got {command[0]}")
            return False
            
        # Check subcommands first
        for cmd in self.commands:
            logger.debug(f"Command.validate: Checking subcommand {cmd.name}")
            if cmd.validate(command[1:]):
                logger.debug(f"Command.validate: Subcommand {cmd.name} validated")
                return True
                
        # If no subcommands match, validate options
        for name, option in self.options.items():
            logger.debug(f"Command.validate: Validating option {name}")
            if option.validate(command[1:]) is False:
                logger.debug(f"Command.validate: Option {name} validation failed")
                return False
                
        logger.debug("Command.validate: All validations passed")
        return True
