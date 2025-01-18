from bettercli import CLI, pos_option

cli = CLI()

@cli.command("greet")
@pos_option("name", str)
def greet(name):
    print(f"Hello, {name}!")
