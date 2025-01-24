from functools import wraps
import sys
import keyboard
import time
import typing as t
from .ansi import ANSIColors, Cursor

import logging

logger = logging.getLogger("bettercli.cl")

T = t.TypeVar("T", bound=dict)


class Dict(dict, t.Generic[T]):
    def __init__(self, dict:'dict', default:'dict'={}):
        self.default = default
        super().__init__(dict)

    def get(self, key:'T', default=None) -> 'T|t.Literal[""]':
        if key in self:
            return self[key]
        elif default is not None:
            return default
        elif key in self.default:
            return self.default[key]
        else:
            return ""

SELECTOR_SYMBOL = t.TypedDict("SELECTOR_SYMBOL",
    {
        "bg-color": str,
        "fg-color": str,
        "symbol": str,
    },
    total=False
)

SELECTOR_STYLE = t.TypedDict("SELECTOR_STYLE",
    {
        "bg-color": str,
        "fg-color": str,
        "symbol": SELECTOR_SYMBOL,
    },
    total=False
)

PROMPT_STYLE = t.TypedDict("PROMPT_STYLE",
    {
        "bg-color": str,
        "fg-color": str,
    },
    total=False
)

CURSOR_STYLE = t.TypedDict("CURSOR_STYLE",
    {
        "bg-color": str,
        "fg-color": str,
        "symbol": str,
    },
    total=False
)

INPUT_STYLE = t.TypedDict("INPUT_STYLE",
    {
        "bg-color": str,
        "fg-color": str,
    },
    total=False
)

INPUT_STYLES = t.TypedDict("INPUT_STYLES",
    {
        "prompt": PROMPT_STYLE,
        "cursor": CURSOR_STYLE,
        "input": INPUT_STYLE,
        "selector": dict[t.Literal["cursor", "not cursor"], SELECTOR_STYLE],
    },
    total=False
)

class Input:
    """A widget that allows the user to enter text"""

    DEFAULT_STYLE:'INPUT_STYLES' = Dict({ # type: ignore
        "prompt": Dict({
            "bg-color": ANSIColors.reset_bg,
            "fg-color": ANSIColors.reset_fg,
        }),
        "cursor": Dict({
            "bg-color": ANSIColors.reset_bg,
            "fg-color": ANSIColors.cyan,
            "symbol": "█",
        }),
        "input": Dict({
            "bg-color": ANSIColors.reset_bg,
            "fg-color": ANSIColors.reset_fg,
        }),
        "selector": Dict({
            "cursor": Dict({
                "fg-color": ANSIColors.cyan,
                "bg-color": ANSIColors.reset_bg,
            }),
            "not cursor": Dict({
                "fg-color": ANSIColors.reset_fg,
                "bg-color": ANSIColors.reset_bg,
            }),
        })
    })
    def __init__(self, prompt: 'str', suggestions: 'list[str]' = None, *, style: 'INPUT_STYLES' = {}):
        self.prompt = prompt
        self.suggestions = suggestions if suggestions is not None else []
        self.input_buffer = []
        self.cursor_pos = 0
        self.current_suggestions: list[str] = []
        self.selected_suggestion = 0
        self.running = True
        self._on_input = lambda x: self.suggestions
        self.validate:'t.Callable[[str], t.Union[str, t.Literal[True]]]' = lambda x: True
        self.style = Dict[INPUT_STYLES](style if style is not None else {}, self.DEFAULT_STYLE) # type: ignore
        self.error = ""

    def on_input(self, filter:'bool'=True, case_sensitive:'bool'=False):
        """Decorator to handle input changes and update suggestions"""
        self.filter = filter
        self.case_sensitive = case_sensitive
        def decorator(func: 't.Callable[[str], list[str]]'):
            self._on_input = func
            @wraps(func)
            def wrapper(input: str):
                return func(input)
            return wrapper
        return decorator
    
    def validator(self):
        def decorator(func: 't.Callable[[str], t.Union[str, t.Literal[True]]]'):
            self.validate = func
            @wraps(func)
            def wrapper(input: str):
                return func(input)
            return wrapper
        return decorator
        
    def set_suggestions(self, suggestions: 'list[str]'):
        """Update the suggestions dictionary"""
        self.suggestions = suggestions
        
    def _get_suggestions(self, text: str) -> 'list[str]':
        """Get matching suggestions based on current input"""
        if not text:
            return []
        if self.filter:
            if self.case_sensitive:
                return [suggestion for suggestion in self._on_input(text) if text in suggestion]
            
            return [suggestion for suggestion in self._on_input(text) if text.lower() in suggestion.lower()]
        else:
            return self._on_input(text)
        
        
    def _print_screen(self):
        """Print the current state of the input and suggestions"""
        
        # Print input line
        input_str = f"{self.style.get("input").get("fg-color")}{self.style.get("input").get("bg-color")}{"".join(self.input_buffer)}{ANSIColors.reset}"
        prompt = f"{self.style.get('prompt').get('fg-color')}{self.style.get('prompt').get('bg-color')}{self.prompt}{ANSIColors.reset}"

        suggestions = []
        for i, suggestion in enumerate(self.current_suggestions):
            type = "cursor" if self.selected_suggestion == i else "not cursor"
            style = f"{self.style.get("selector").get(type).get("fg-color")}{self.style.get('selector').get(type).get("bg-color")}"
            suggestions.append(f"{style}{suggestion}{ANSIColors.reset}")

        sys.stdout.write(f"{Cursor.clear_screen}{Cursor.goto()}{prompt}{input_str}{self.style.get("cursor").get("fg-color")}{self.style.get('cursor').get("bg-color")}{self.style.get('cursor').get("symbol")}{ANSIColors.reset}\n{"\n".join(suggestions)}\n{self.error}{Cursor.goto(1, (len("".join(self.input_buffer)) + len(self.prompt)))}")
        sys.stdout.flush()
        
    def _handle_input(self, event):
        """Handle keyboard input events"""
        def input():
            current_text = "".join(self.input_buffer)
            self.current_suggestions = self._get_suggestions(current_text)
            self.selected_suggestion = 0

        
        if event.name == "enter":
            self.running = False
            return
            
        elif event.name == "backspace":
            if self.cursor_pos > 0:
                self.input_buffer.pop(self.cursor_pos - 1)
                self.cursor_pos -= 1
                input()
                
        elif event.name == "space":
            self.input_buffer.insert(self.cursor_pos, " ")
            self.cursor_pos += 1
            input()
            
        elif event.name == "tab":
            if self.current_suggestions:
                suggestion = self.current_suggestions[self.selected_suggestion]
                self.input_buffer = list(suggestion)
                self.cursor_pos = len(suggestion)
                input()
            else:
                self.input_buffer.insert(self.cursor_pos, "    ")
                
        elif event.name == "up" and self.current_suggestions:
            self.selected_suggestion = max(0, self.selected_suggestion - 1)
            
        elif event.name == "down" and self.current_suggestions:
            self.selected_suggestion = min(len(self.current_suggestions)-1, self.selected_suggestion + 1)
            
        elif event.name == "left":
            self.cursor_pos = max(0, self.cursor_pos - 1)
            input()
            
        elif event.name == "right":
            self.cursor_pos = min(len(self.input_buffer), self.cursor_pos + 1)
            input()
            
        elif len(event.name) == 1:  # Regular character
            self.input_buffer.insert(self.cursor_pos, event.name)
            self.cursor_pos += 1
            input()
        
        # Redraw screen
        self._print_screen()
        
    def run(self) -> str:
        """Run the autocomplete input loop"""
        keyboard.on_press(self._handle_input, suppress=True)
        Cursor.write.hide_cursor()
        self._print_screen()
        validated = False
        while not validated:
            self.running = True
            while self.running:
                time.sleep(0.1)
            
            if (error := self.validate("".join(self.input_buffer))) is not True:
                logger.debug(f"Input: {''.join(self.input_buffer)} failed: {error}")
                self.error = error
                self.selected_suggestion = 0
                self.cursor_pos = 0
                self.input_buffer = []
                self._print_screen()
            else:
                logger.debug(f"Input: {''.join(self.input_buffer)} success")
                validated = True

        Cursor.write.show_cursor()
        return "".join(self.input_buffer)