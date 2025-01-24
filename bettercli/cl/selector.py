from . import Cursor
import typing as t
import keyboard
import sys
import time

from .ansi import ANSIColors

SYMBOL = t.TypedDict("SYMBOL",
    {
        "bg-color": str,
        "fg-color": str,
        "symbol": str,
    },
    total=False
)

STYLES = t.TypedDict("STYLES",
    {
        "bg-color": str,
        "fg-color": str,
        "symbol": SYMBOL,
    },
    total=False
)



class Selector:
    """
    A selector for selecting an option from a list of options.
    Args:
        options (dict[str, str]): A dictionary of options, where the keys are the option names and the values are the option descriptions.
        symbol (str, optional): The symbol to use for the selector. Defaults to "*".
        style (dict[Union[str, Literal["ALL", "NONE", "SELECTED", "NOT SELECTED"]], STYLES], optional): A dictionary of styles for the selector. Defaults to {"SELECTED": Selector.DEFAULT_SELECTED, "NOT SELECTED": Selector.DEFAULT_NOT_SELECTED}.
        keybinds (dict[str, Callable[[Selector, str], None]], optional): A dictionary of keybinds for the selector. Defaults to {"left": Selector.select_all, "right": Selector.unselect_all, "up": Selector.up, "down": Selector.down, "space": Selector.toggle, "enter": Selector.enter}.
        max (int, optional): The maximum number of options that can be selected. Defaults to -1.
        min (int, optional): The minimum number of options that must be selected. Defaults to 1.
    """

    def select(self, key: 'str'):
        self.selected.append(key)

    def unselect(self, key: 'str'):
        self.selected.remove(key)

    def toggle(self, key: 'str'):
        if key in self.selected:
            self.unselect(key)
        else:
            self.select(key)
        
    def select_all(self, key):
        if self.max == 1:
            self.select(key)
        self.selected = self.keys.copy()

    def unselect_all(self, key):
        self.selected.clear()

    def enter(self, key):
        self.ENTERED = True

    def up(self, key):
        try:
            self.key = self.keys[self.keys.index(key) - 1]
        except IndexError:
            self.key = self.keys[0]

    def down(self, key):
        try:
            self.key = self.keys[self.keys.index(key) + 1]
        except IndexError:
            self.key = self.keys[-1]

    def select_and_enter(self, key):
        self.select(key)
        self.enter(key)

    STYLE = dict[t.Union[str, t.Literal["ALL", "NONE", "SELECTED", "NOT SELECTED", "CURSOR", "NOT CURSOR"]], STYLES]
    DEFAULT_SELECTED:'STYLES' = {
        "symbol": {
            "bg-color": ANSIColors.reset_bg,
            "fg-color": ANSIColors.reset_fg,
            "symbol": "●",
        }
    }
    DEFAULT_CURSOR:'STYLES' = {
        "bg-color": ANSIColors.reset_bg,
        "fg-color": ANSIColors.cyan,
    }
    DEFAULT_NOT_CURSOR:'STYLES' = {
        "bg-color": ANSIColors.reset_bg,
        "fg-color": ANSIColors.reset_fg,
    }
    DEFAULT_NOT_SELECTED:'STYLES' = {
        "symbol": {
            "bg-color": ANSIColors.reset_bg,
            "fg-color": ANSIColors.reset_fg,
            "symbol": "○",
        }
    }

    DEFAULT_KEYBINDS = {
        "left": select_all,
        "right": unselect_all,
        "up": up,
        "down": down,
        "space": toggle,
        "enter": enter,
    }

    def __init__(self, options: 'dict[str, str]', question:'str'="", *, style: 'STYLE | None' = None, keybinds: 'dict[str, t.Callable[[t.Self, str], None]]' = DEFAULT_KEYBINDS, max:'int'=-1, min:'int'=1, validator:'t.Callable[[list[str]], t.Union[str, t.Literal[True]]]'=lambda x: True):  
        assert isinstance(options, dict), "Options must be a dictionary"
        self.options = options
        self.selected = []
        self.ALL = False
        self.NONE = True
        self.ENTERED = False
        self.style:'Selector.STYLE' = {}
        self.keybinds = keybinds
        self.max = max
        self.min = min
        self.question = question
        self._validator = validator
        self.error = ""

        
        self.style["SELECTED"] = {**self.DEFAULT_SELECTED, **self.style.get("SELECTED", {})}
        self.style["NOT SELECTED"] = {**self.DEFAULT_NOT_SELECTED, **self.style.get("NOT SELECTED", {})}
        self.style["CURSOR"] = {**self.DEFAULT_CURSOR, **self.style.get("CURSOR", {})}
        self.style["NOT CURSOR"] = {**self.DEFAULT_NOT_CURSOR, **self.style.get("NOT CURSOR", {})}


    def handler(self, key):
        if key.name in self.keybinds:
            self.keybinds[key.name](self, self.key)
            self.print()

    def validator(self):
        def wrapper(func:'t.Callable[[list[str]], t.Union[str, t.Literal[True]]]'):
            self._validator = func
            def decorator(options:'list[str]'):
                return func(options)
            return decorator
        return wrapper

    def run(self, *, sleep:'float'=0.1):
        """Run the selector."""
        Cursor.hide_cursor()
        self.keys = list(self.options.keys())
        self.key = self.keys[0]

        sys.stdout.write(ANSIColors.reset)
        self.print()
        keyboard.on_press(self.handler, suppress=True)
        validated = False
        while not validated:
            while not self.ENTERED:
                pass
            if (validate := self._validator(self.selected)) != True:
                self.error = validate
                self.ENTERED = False
                self.print()
            else:
                validated = True
        time.sleep(sleep) # Add a small sleep to prevent UI from being weird sometimes
        Cursor.show_cursor()
        return self.selected
    

    def print(self):
        """Print the selector."""

        selector = f"{self.question}\n\n" if self.question else ""
        for key, option in self.options.items():
            style = self.style["SELECTED" if key in self.selected else "NOT SELECTED"]
            if self.ALL and "ALL" in self.style:
                style.update(self.style["ALL"])
            elif self.NONE and "NONE" in self.style:
                style.update(self.style["NONE"])
            
            if key in self.style:
                style.update(self.style[key])

            cursor_style = self.style["CURSOR" if key == self.key else "NOT CURSOR"]
            style.update(cursor_style)

            assert "symbol" in style, "Symbol must be a style"
            s = style["symbol"]
            assert "symbol" in s, "Symbol must be a style"

            symbol = s["symbol"]
            if "fg-color" in s:
                symbol = f"{s['fg-color']}{symbol}"
            if "bg-color" in s:
                symbol = f"{s['bg-color']}{symbol}"
            symbol = f"{symbol}{ANSIColors.reset}"

            if "fg-color" in style:
                option = f"{style['fg-color']}{option}"
            if "bg-color" in style:
                option = f"{style['bg-color']}{option}"
            
            if "fg-color" in cursor_style:
                symbol = f"{cursor_style['fg-color']}{symbol}"
            if "bg-color" in cursor_style:
                symbol = f"{cursor_style['bg-color']}{symbol}"
            selector += f"{symbol} {option}{ANSIColors.reset}\n"
        
        if self.error:
            selector += f"\n{self.error}\n"

        sys.stdout.write("\033[2J\033[H")
        sys.stdout.write(selector)
        sys.stdout.flush()

    def set_question(self, question:'str'):
        self.question = question

    def set_options(self, options:'dict[str, str]'):
        self.options = options

class SingleSelector(Selector):
    DEFAULT_NOT_SELECTED = {
        "symbol": {
            "symbol": ""
        },
    }
    DEFAULT_SELECTED = {
        "symbol": {
            "symbol": "",
        },
    }

    def up(self, key):
        return super().up(key)
    
    def down(self, key):
        return super().down(key)
    
    def select_and_enter(self, key):
        return super().select_and_enter(key)

    DEFAULT_KEYBINDS = {
        "up": up,
        "down": down,
        "enter": select_and_enter,
    }

    def __init__(self, options: 'dict[str, str]', question:'str'="", *, style: 'Selector.STYLE | None' = None, keybinds: 'dict[str, t.Callable[[t.Self, str], None]]' = DEFAULT_KEYBINDS, validator:'t.Callable[[list[str]], t.Union[str, t.Literal[True]]]'=lambda x: True): # type: ignore
        print(keybinds)
        super().__init__(options, question, style=style, keybinds=keybinds, max=1, min=1, validator=validator)

    def run(self, sleep:'float'=0.1) -> 'str': # type: ignore
        return super().run(sleep=sleep)[0]
