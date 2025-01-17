import sys
import logging

from bettercli.command import Command


logger = logging.getLogger("bettercli")

class CLI:
    """
    A class that represents a command-line interface.

    The CLI class provides functionality to create and run command-line applications.
    It allows adding commands using decorators or directly, and handles command execution.

    Attributes:
        commands (list[Command]): List of registered Command objects that can be executed.

    Example:
        >>> cli = CLI()
        >>> @cli.command("greet")
        ... def greet(name):
        ...     print(f"Hello {name}!")
        >>> cli.run()
    """
    commands: 'list[Command]' = []

    def add_command(self, command: 'Command'):
        self.commands.append(command)

    def command(self, name: 'str'):
        def decorator(func):
            command = Command(name=name, callback=func)
            self.add_command(command)
            return command
        return decorator

    def run(self):
        logger.debug("Running CLI")
        command_args = sys.argv[1:]
        for cmd in self.commands:
            if cmd.validate(command_args):
                cmd.run(command_args)
                return
