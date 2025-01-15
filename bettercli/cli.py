import sys
import logging

from bettercli.command import Command


logger = logging.getLogger("bettercli")

class CLI:
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
            cmd.run(command_args)
