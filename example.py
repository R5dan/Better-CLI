from bettercli import CLI, kw_option, pos_option, logger
from bettercli.option import InvalidLength

logger.disable_debug()

cli = CLI()



# Here's the corrected version:
@pos_option("name", str, length=1, default="World") 
@cli.command("greet")
def greet(name):
    if isinstance(name, InvalidLength):
        print(f"Invalid length for name: {name}")
        print(name.op)
        print(name.option.validate([name.op]))
        return
    print(f"Hello {name}!")

@kw_option("x", int, "-x", "--x", length=2, default=0)
@kw_option("y", int, "-y", "--y", length=2, default=0)
@cli.command("add")
def add(x=0, y=0):
    print(f"{x} + {y} = {x+y}")

if __name__ == "__main__":
    cli.run()
