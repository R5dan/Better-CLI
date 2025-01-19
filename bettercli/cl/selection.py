import typing as t
from colorama import Fore, Style, Back, Cursor

SELECTOR_STYLE = t.TypedDict("SELECTOR_STYLE", {"bg-color": str, "fg-color": str, "symbol": str}, total=False)
TEXT_STYLE = t.TypedDict("TEXT_STYLE", {"bg-color": str, "fg-color": str, "bold": bool, "italic": bool, "underline": bool}, total=False)
STYLES = t.TypedDict("STYLES", {"selector": SELECTOR_STYLE, "text": TEXT_STYLE}, total=False)


class Selector:
    def __init__(self, options:'list[str]', *, symbol:'str'="*", style:'dict[t.Union[int, t.Literal["ALL", "NONE", "SELECTED", "NOT SELECTED"]], STYLES]'=None):
        self.options = options
        self.symbol = symbol
        self.style = style

    def run(self):
        
        for index, option in enumerate(self.options):
            print(f"{self.symbol.format(index=index)} {option}")