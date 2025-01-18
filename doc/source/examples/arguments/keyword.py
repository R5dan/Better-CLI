from bettercli import CLI, kw_option

cli = CLI()

@kw_option("x", int, "-x", "--x", length=2, default=0)
@kw_option("y", int, "-y", "--y", length=2, default=0)
@cli.command("add")
def add(x=0, y=0):
    print(f"{x} + {y} = {x+y}")