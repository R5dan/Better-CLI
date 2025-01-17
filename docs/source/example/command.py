from bettercli import CLI

cli = CLI()

@cli.command("greet")
def greet():
    print("Hello, world!")

