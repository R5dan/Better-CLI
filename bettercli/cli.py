import sys
import logging
import typing as t

from bettercli.command import Command
from bettercli.exceptions import InvalidCommand, BetterCLIException

class DefaultCallback(t.Protocol):
    def __call__(self, *args, **kwargs) -> None: ...


logger = logging.getLogger("bettercli")

class CLI:
    def __init__(self):
        self.commands: 'dict[str, Command]' = {}
        self.default_callback:'t.Union[DefaultCallback, None]' = None


    def add_command(self, name:'str', command: 'Command'):
        self.commands[name] = command

    def command(self, name: 'str'):
        def decorator(func):
            command = Command(name=name, callback=func)
            self.add_command(name, command)
            return command
        return decorator
    
    def default(self):
        def decorator(func:'DefaultCallback'):
            self.default_callback = func
            return func
        return decorator

    def run(self):
        logger.debug(
            """

-----------
Running CLI
-----------

            """
            )
        command_args = sys.argv[1:]

        try:
            logger.debug(f"CLI.run: Running command: {command_args[0]=} {command_args=}")
            cmd = self.commands.get(command_args[0], None)
            if cmd is None:
                if self.default_callback is not None:
                    logger.debug(f"CLI.run: Running default callback: {self.default_callback=}")
                    kwargs = {}
                    args = []
                    kws = False
                    kw = ""
                    kw_args = []
                    for arg in command_args:
                        if arg.startswith("-"):
                            if kws == True:
                                kwargs[kw] = kw_args
                                kw_args = []

                            kws = True
                            kw = arg
                        else:
                            if kws == True:
                                kw_args.append(arg)
                            else:
                                args.append(arg)


                    self.default_callback(*args, **kwargs)
                else:
                    raise InvalidCommand(None, command_args)
            else:
                cmd.run(command_args)
        except InvalidCommand as e:
            logger.debug(f"CLI.run: InvalidCommand: {e}")
            print(e.to_cli())
        except BetterCLIException as e:
            logger.debug(f"CLI.run: BetterCLIException: {e}")
            print(e.to_cli())

