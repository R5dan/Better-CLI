import typing as t
import logging

from .option import Keyword_option, Positional_option
from .exceptions import InvalidLength, InvalidType, InvalidCommand, TooManyOccurrences

T = t.TypeVar("T")
logger = logging.getLogger("bettercli")

@t.runtime_checkable
class Callback(t.Protocol):
    def __call__(self, **kwargs) -> None: ...

class Command:
    def __init__(self, name:'str', callback:'Callback'=lambda **kwargs: None, allow_extra=False):
        logger.debug(f"Command.__init__: {name=} {callback=}")
        self.name = name
        self._callback = callback
        self.allow_extra = allow_extra
        self.pos_options:'list[Positional_option]' = []
        self.kw_options:'dict[str, Keyword_option]' = {}
        self.commands: 'list[Command]' = []
        self.perm_args = {}

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


    def add_positional_option(self, name:'str', type_:'type[T]', default:'T', *, length:'int'=1):
        logger.debug(f"Command.add_positional_option: {name=} {type_=} {default=} {length=}")
        if any(option.name == name for option in self.pos_options):
            raise ValueError(f"{name} already defined. {name} is a {type(self.pos_options[name]).__name__} with type {self.pos_options[name].type}")
        elif name in self.kw_options:
            raise ValueError(f"{name} already defined. {name} is a {type(self.kw_options[name]).__name__} with type {self.kw_options[name].type}")
        option = Positional_option(name, type_, default=default, length=length)
        self.pos_options.append(option)

    def add_keyword_option(self, name, _type, default, *kws, length:'int'=2, max_occurrences:'int'=1):
        logger.debug(f"Command.add_keyword_option: {name=} {_type=} {default=} {kws=} {length=} {max_occurrences=}")
        if name in self.kw_options:
            raise ValueError(f"{name} already defined. {name} is a {type(self.kw_options[name]).__name__} with type {self.kw_options[name].type}")
        elif any(option.name == name for option in self.pos_options):
            raise ValueError(f"{name} already defined. {name} is a {type(self.pos_options[name]).__name__} with type {self.pos_options[name].type}")
        

        if any(kw in self.kw_options for kw in kws):
            reused = [kw for kw in kws if kw in self.kw_options]
            raise ValueError(f"Keyword option(s) {reused} already defined.")

        option = Keyword_option(name, _type, *kws, default=default, length=length, max_occurrences=max_occurrences)
        self.kw_options.update({kw: option for kw in kws})

    @property
    def schema(self):
        logger.debug("Command.schema")
        return [self.name] + [option.name for option in self.pos_options]
        
    def run(self, command:'list[str]', perm_args:'dict[str, t.Any]'={}):
        logger.debug(f"Command.run: {command=} {self.kw_options=} {self.pos_options=}")
        name = command.pop(0)
        if name != self.name:
            raise InvalidCommand(self, command)
        
        if len(command) >= 2 and command[1] in self.commands:
            logger.debug(f"Command.run: Command {command[1]} is a subcommand")
            self.commands[command[1]].run(command[1:])

        def check_all_pos_args(args:'dict[str, t.Any]', options:'list[Positional_option]') -> 'dict[str, t.Any]':
            logger.debug(f"check_all_pos_args: {args=}, {options=}")
            for option in options:
                logger.debug(f"check_all_pos_args: option: {option}")
                if option.name not in args:
                    logger.debug(f"check_all_pos_args: option.name not in args: {option.name}")
                    if option.has_default == False:
                        logger.debug(f"check_all_pos_args: option.has_default == False: {option.name}")
                        raise InvalidCommand(self, command)
                    logger.debug(f"check_all_pos_args: default: {option.default}")
                    args[option.name] = option.default
                logger.debug(f"check_all_pos_args: {option.name} in {args}")
            return args

        if (len(self.pos_options) > 0) and (len(command) >= 1) and (not command[0].startswith("-")):
            options = {}
            option = self.pos_options[0]
            cur_option = []
            op_index = 0
            kw = False
            for cmd in command:
                logger.debug(f"Command.run: cmd: {cmd}, cur_option: {cur_option}")
                if cmd.startswith("-"):
                    logger.debug(f"KW arg found: {cmd}")
                    kw = True
                    index = command.index(cmd)
                    break

                op, change = option.validate(cmd, cur_option)
                if isinstance(op, (InvalidType, InvalidLength)):
                    raise op
                
                if change:
                    if len(cur_option) == 1:
                        options[option.name] = cur_option[0]
                    else:
                        options[option.name] = cur_option
                    
                    cur_option = []
                    option = self.pos_options[op_index]
                    op_index += 1


        else:
            logger.debug(f"Command.run: No positional options, {len(self.pos_options)=} {command=} {len(command)=}")
            options = check_all_pos_args({}, self.pos_options)
            kw = False
            if len(command) > 0 and command[0].startswith("-"):
                kw = True
                index = 0

            

        if kw:
            args = [command[index]] # type: ignore
            option = self.kw_options[command[index]] # type: ignore
            logger.debug(f"TEST {command} {command[index]} {command[index+1]}")
            for cmd in command[index+1:]: # type: ignore    I know that index is set if kw is true
                logger.debug(f"KW arg: {cmd}")
                if cmd.startswith("-"):
                    logger.debug(f"New keyword option: {cmd}. Args: {args}")
                    if options.get(option.name, None) is None:
                        options[option.name] = []

                    validated = option.validate(args)
                    if isinstance(validated, (InvalidType, InvalidLength, TooManyOccurrences)):
                        raise validated

                    if option.occurrences == 1:
                        options[option.name] = validated
                    else:
                        options[option.name].append(validated)

                    option = self.kw_options[cmd]
                    args = [cmd]
                    
                else:
                    logger.debug(f"Adding {cmd} to args: {args}")
                    args.append(cmd)

            logger.debug(f"Command.run: Finished parsing args")

            if options.get(option.name, None) is None:
                options[option.name] = []

            validated = option.validate(args)
            if isinstance(validated, (InvalidType, InvalidLength, TooManyOccurrences)):
                raise validated

            if option.occurrences == 1:
                options[option.name] = validated
            else:
                options[option.name].append(validated)
            
        logger.debug(f"Command.run: Calling callback with options: {options}")
        self.callback(**options)

    def __repr__(self):
        return f"<Command {self.name}>"