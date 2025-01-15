# BetterCLI

A Python library for building better command-line interfaces with ease.

## Installation
You can install BetterCLI using pip:

```bash
pip install bettercli
```

## Example

```python
from bettercli import CLI, pos_option, kw_option

cli = CLI()

@cli.command("greet")
def greet(name):
    print(f"Hello {name}!")
    
@pos_option("name", str, length=1, default="World")
@cli.command("greet")
def greet(name):
    print(f"Hello {name}!")
```

## License
BetterCLI is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
