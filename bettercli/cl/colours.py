SYMBOL = "\033[{}m"

class ANSIColors:    
    @staticmethod
    def rgb(r, g, b, background=False):
        """Convert RGB to ANSI escape sequence"""
        return SYMBOL.format(f"{48 if background else 38};2;{r};{g};{b}")
    
    @staticmethod
    def color_256(code, background=False):
        """Use 256 color mode"""
        return SYMBOL.format(f"{48 if background else 38};5;{code}")
        

    reset = SYMBOL.format(0)

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