from functools import wraps
import sys
import keyboard
import time
import typing as t
from . import colours as c

T = t.TypeVar("T", bound=dict)


class Dict(dict, t.Generic[T]):
    def __init__(self, dict:'dict', default:'dict'={}):
        self.default = default
        super().__init__(dict)

    def get(self, key:'T', default=None) -> 'T|None':
        if key in self:
            return self[key]
        elif default is not None:
            return default
        elif key in self.default:
            return self.default[key]
        else:
            return None

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
        "on": bool,
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
            "bg-color": c.ANSIColors.reset,
            "fg-color": c.ANSIColors.reset,
        }),
        "cursor": Dict({
            "bg-color": c.ANSIColors.reset,
            "fg-color": c.ANSIColors.cyan,
            "symbol": "█",
            "on": False,
        }),
        "input": Dict({
            "bg-color": c.ANSIColors.reset,
            "fg-color": c.ANSIColors.reset,
        }),
        "selector": Dict({
            "cursor": Dict({
                "fg-color": c.ANSIColors.cyan,
            }),
            "not cursor": Dict({
                "fg-color": c.ANSIColors.reset,
            }),
        })
    })
    def __init__(self, prompt: str, suggestions: dict[str, str] = None, *, style: 'INPUT_STYLES' = {}):
        self.prompt = prompt
        self.suggestions = suggestions or {}
        self.input_buffer = []
        self.cursor_pos = 0
        self.current_suggestions: dict[str, str] = {}
        self.selected_suggestion = 0
        self.running = True
        self._on_input = lambda x: self.suggestions
        self.validate = lambda x: True
        self.style = Dict[INPUT_STYLES](style, self.DEFAULT_STYLE) # type: ignore
        
    def on_input(self):
        """Decorator to handle input changes and update suggestions"""
        def decorator(func: t.Callable[[str], dict[str, str]]):
            self._on_input = func
            @wraps(func)
            def wrapper(input: str):
                return func(input)
            return wrapper
        return decorator
    
    def validator(self):
        def decorator(func: t.Callable[[str], t.Union[str, t.Literal[True]]]):
            self.validate = func
            @wraps(func)
            def wrapper(input: str):
                return func(input)
            return wrapper
        return decorator
        
    def set_suggestions(self, suggestions: dict[str, str]):
        """Update the suggestions dictionary"""
        self.suggestions = suggestions
        
    def _get_suggestions(self, text: str) -> dict[str, str]:
        """Get matching suggestions based on current input"""
        if not text:
            return {}
        suggestions = self._on_input(text)
        return {k:v for k,v in suggestions.items() 
               if k.lower().startswith(text.lower())}
        
    def _print_screen(self):
        """Print the current state of the input and suggestions"""
        # Clear screen
        sys.stdout.write("\033[2J\033[H")
        
        # Print input line
        input_str = f"{self.style.get("input").get("fg-color")}{self.style.get("input").get("bg-color")}{"".join(self.input_buffer)}{c.ANSIColors.reset}"
        prompt = f"{self.style.get('prompt').get('fg-color')}{self.style.get('prompt').get('bg-color')}{self.prompt}{c.ANSIColors.reset}"

        suggestions = []
        for i, (_, description) in enumerate(self.current_suggestions.items()):
            type = "cursor" if self.selected_suggestion == i else "not cursor"
            style = f"{self.style.get("selector").get(type).get("fg-color")}{self.style.get('selector').get(type).get("bg-color")}"
            suggestions.append(f"{style}{description}{c.ANSIColors.reset}")

        sys.stdout.write(f"{prompt}{input_str}\n{"".join(suggestions)}")


        # Move cursor back to input
        sys.stdout.write(f"\033[{len(self.current_suggestions)+1}A")
        sys.stdout.write(f"\033[{len(self.prompt) + self.cursor_pos}C")
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
                suggestion = list(self.current_suggestions.keys())[self.selected_suggestion]
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
        self._print_screen()
        
        while self.running:
            time.sleep(0.1)
        
        print()  
        return "".join(self.input_buffer)