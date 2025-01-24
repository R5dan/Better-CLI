import sys

class ANSIColors:    
    @classmethod
    def rgb(cls, r, g, b, background=False):
        """Convert RGB to ANSI escape sequence"""
        return cls.SYMBOL.format(f"{48 if background else 38};2;{r};{g};{b}")
    
    @classmethod
    def color_256(cls, code, background=False):
        """Use 256 color mode"""
        return cls.SYMBOL.format(f"{48 if background else 38};5;{code}")
    
    SYMBOL = "\033[{}m"

    reset = SYMBOL.format(0)

    reset_fg = SYMBOL.format(39)
    reset_bg = SYMBOL.format(49)
    reset_text_effects = SYMBOL.format(20)


    # Standard foreground colors (30-37)
    black = SYMBOL.format(30)
    red = SYMBOL.format(31)
    green = SYMBOL.format(32)
    yellow = SYMBOL.format(33)
    blue = SYMBOL.format(34)
    magenta = SYMBOL.format(35)
    cyan = SYMBOL.format(36)
    white = SYMBOL.format(37)
    gray = SYMBOL.format(90)
    
    # Standard background colors (40-47)
    bg_black = SYMBOL.format(40)
    bg_red = SYMBOL.format(41)
    bg_green = SYMBOL.format(42)
    bg_yellow = SYMBOL.format(43)
    bg_blue = SYMBOL.format(44)
    bg_magenta = SYMBOL.format(45)
    bg_cyan = SYMBOL.format(46)
    bg_white = SYMBOL.format(47)
    bg_gray = SYMBOL.format(100)
    
    # Bright foreground colors (90-97)
    bright_black = SYMBOL.format(90)
    bright_red = SYMBOL.format(91)
    bright_green = SYMBOL.format(92)
    bright_yellow = SYMBOL.format(93)
    bright_blue = SYMBOL.format(94)
    bright_magenta = SYMBOL.format(95)
    bright_cyan = SYMBOL.format(96)
    bright_white = SYMBOL.format(97)
    
    # Bright background colors (100-107)
    bg_bright_black = SYMBOL.format(100)
    bg_bright_red = SYMBOL.format(101)
    bg_bright_green = SYMBOL.format(102)
    bg_bright_yellow = SYMBOL.format(103)
    bg_bright_blue = SYMBOL.format(104)
    bg_bright_magenta = SYMBOL.format(105)
    bg_bright_cyan = SYMBOL.format(106)
    bg_bright_white = SYMBOL.format(107)
    
    # Text effects
    bold = SYMBOL.format(1)
    dim = SYMBOL.format(2)
    italic = SYMBOL.format(3)
    underline = SYMBOL.format(4)
    blink = SYMBOL.format(5)
    reverse = SYMBOL.format(7)
    hidden = SYMBOL.format(8)
    strike = SYMBOL.format(9)
    double_underline = SYMBOL.format(21)
    overline = SYMBOL.format(53)
    
    # Additional colors using color_256 method
    orange = color_256(208)
    pink = color_256(213)
    purple = color_256(93)
    brown = color_256(130)
    lime = color_256(118)
    teal = color_256(30)
    navy = color_256(17)
    maroon = color_256(88)
    turquoise = color_256(45)
    lavender = color_256(183)
    coral = color_256(209)
    olive = color_256(100)
    
    # Background versions
    bg_orange = color_256(208, background=True)
    bg_pink = color_256(213, background=True)
    bg_purple = color_256(93, background=True)
    bg_brown = color_256(130, background=True)
    bg_lime = color_256(118, background=True)
    bg_teal = color_256(30, background=True)
    bg_navy = color_256(17, background=True)
    bg_maroon = color_256(88, background=True)
    bg_turquoise = color_256(45, background=True)
    bg_lavender = color_256(183, background=True)
    bg_coral = color_256(209, background=True)
    bg_olive = color_256(100, background=True)



class CursorWrite:
    @staticmethod
    def hide_cursor():
        sys.stdout.write(Cursor.hide_cursor)
    
    @staticmethod
    def show_cursor():
        sys.stdout.write(Cursor.show_cursor)

    @staticmethod
    def up(n=1):
        sys.stdout.write(Cursor.up(n))
    
    @staticmethod
    def down(n=1):
        sys.stdout.write(Cursor.down(n))
    
    @staticmethod
    def right(n=1):
        sys.stdout.write(Cursor.right(n))

    @staticmethod
    def left(n=1):
        sys.stdout.write(Cursor.left(n))
    
    @staticmethod
    def goto(x=1, y=1):
        sys.stdout.write(Cursor.goto(x, y))

    @staticmethod
    def beginning_of_line(n=0):
        """Move cursor to the beginning of the line n lines down"""
        sys.stdout.write(Cursor.beginning_of_line(n))

    @staticmethod
    def start_of_line(n=0):
        """Move cursor to the beginning of the line n lines up"""
        sys.stdout.write(Cursor.start_of_line(n))

    @staticmethod
    def save():
        sys.stdout.write(Cursor.save)

    @staticmethod
    def restore():
        sys.stdout.write(Cursor.restore)
    
    @staticmethod
    def clear_line_from_cursor():
        sys.stdout.write(Cursor.clear_line_from_cursor)

    @staticmethod
    def clear_line_to_cursor():
        sys.stdout.write(Cursor.clear_line_to_cursor)

    @staticmethod
    def clear_line():
        sys.stdout.write(Cursor.clear_line)

    @staticmethod
    def clear_screen_from_cursor():
        sys.stdout.write(Cursor.clear_screen_from_cursor)

    @staticmethod
    def clear_screen_to_cursor():
        sys.stdout.write(Cursor.clear_screen_to_cursor)

    @staticmethod
    def clear_screen():
        sys.stdout.write(Cursor.clear_screen)

class Cursor:
    write = CursorWrite()

    
    hide_cursor = "\033[?25l"
    
    show_cursor = "\033[?25h"
    
    @staticmethod
    def up(n=1):
        return f"\033[{n}A"
    
    @staticmethod
    def down(n=1):
        return f"\033[{n}B"
    
    @staticmethod
    def right(n=1):
        return f"\033[{n}C"
    
    @staticmethod
    def left(n=1):
        return f"\033[{n}D"
    
    @staticmethod
    def goto(x=1, y=1):
        return f"\033[{y};{x}H"

    @staticmethod
    def beginning_of_line(n=0):
        """Move cursor to the beginning of the line n lines down"""
        return f"\033[{n}E"
    
    @staticmethod
    def start_of_line(n=0):
        """Move cursor to the beginning of the line n lines up"""
        return f"\033[{n}F"
    
    save = "\033[s"

    restore = "\033[u"
    
    clear_line_from_cursor = "\033[K"

    clear_line_to_cursor = "\033[1K"

    clear_line = "\033[2K"

    clear_screen_from_cursor = "\033[J"

    clear_screen_to_cursor = "\033[1J"

    clear_screen = "\033[2J"
