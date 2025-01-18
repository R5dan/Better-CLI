from bettercli import CLI, kw_option, pos_option


cli = CLI()




@pos_option("name", str, length=1, default="World")
@cli.command("greet")
def greet(name):
    print(f"Hello {name}!")

@kw_option("x", int, "-x", "--x", length=1, default=0)
@kw_option("y", int, "-y", "--y", length=1, default=0)
@cli.command("add")
def add(x, y):
    print(f"{x} + {y} = {x+y}")

if __name__ == "__main__":
    cli.run()
