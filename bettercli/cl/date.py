from datetime import (
    date as d,
    timedelta as td,
)
import time
import typing as t
import sys
import keyboard
from logging import getLogger
from .ansi import Cursor, ANSIColors

logger = getLogger("bettercli.cl")

T = t.TypeVar("T")
LEN = t.TypeVar("LEN", bound=int, default=int)
L = t.TypeVar("L", bound=list)

class LenList(t.Generic[L, LEN], list):
    def __init__(self, length:'LEN', list:'L'=None):
        if list is None:
            list = []
        self.length = length
        super().__init__(list)

    def __len__(self) -> 'LEN':
        return self.length
    
    def copy(self) -> 'LenList[L, LEN]':
        return LenList(self.length, super().copy())
    
class POS:
    def __init__(self, x:'int', y:'int', month:'int', year:'int'):
        self.x = x
        self.y = y
        self.month = month
        self.year = year

    @property
    def xy(self) -> 'tuple[int, int]':
        return self.x, self.y
    
    @xy.setter
    def xy(self, value):
        self.x, self.y = value
    
    @property
    def day(self) -> 'int':
        return self.y *7 + self.x
    
    @property
    def date(self) -> 'd':
        return d(self.year, self.month, self.day)
    
    def compare(self, other:'POS', equal:'bool', gt:'bool'=False, lt:'bool'=False) -> 'bool':
        if self.year > other.year:
            return gt
        elif self.year < other.year:
            return lt
        elif self.month > other.month:
            return gt
        elif self.month < other.month:
            return lt
        elif self.y > other.y:
            return gt
        elif self.y < other.y:
            return lt
        elif self.x > other.x:
            return gt
        elif self.x < other.x:
            return lt
        else:
            return equal

    
    def __gt__(self, other:'POS') -> 'bool':
        return self.compare(other, equal=False, gt=True, lt=False)

    
    def __lt__(self, other:'POS') -> 'bool':
        return self.compare(other, equal=False, gt=False, lt=True)
    
    def __ge__(self, other:'POS') -> 'bool':
        return self.compare(other, equal=True, gt=True, lt=False)
    
    def __le__(self, other:'POS') -> 'bool':
        return self.compare(other, equal=True, gt=False, lt=True)
    
    def __str__(self):
        return f"({self.x},{self.y}) {self.month} {self.year}"
    
    def copy(self):
        return POS(self.x, self.y, self.month, self.year)
    
    def between(self, other:'POS') -> 'list[d]':
        if self > other:
            return other.between(self)
        days = []
        day = d(self.year, self.month, self.day)
        while True:
            if not day == other.date:
                days.append(day)
                break
            days.append(day)
            day += td(days=1)
        
        return days

    
    

class Cache:
    cache:'dict[int, dict[int, list[list[d]]]]' = {}
    def add(self, month:'int', year:'int', days:'list[list[d]]'):
        self.cache[year][month] = days

    def get(self, month:'int', year:'int', raise_:'bool'=False) -> 'list[list[d]]':
        try:
            return self.cache[year][month]
        except KeyError:
            if raise_:
                raise
            self.cache[year][month] = []
            return []
    
    def get_or_add(self, month:'int', year:'int', func:'t.Callable[[int, int], list[list[d]]]'):
        if year not in self.cache:
            self.cache[year] = {}
        if month not in self.cache[year]:
            self.cache[year][month] = func(month, year)
        return self.cache[year][month]
    
DKT = t.TypeVar("DKT", bound=t.Any)
DVT = t.TypeVar("DVT", bound=t.Any)

class Dict(dict):
    def __init__(self, dict:'dict[DKT, DVT]'=None, default:'dict[DKT, DVT]'=None):
        if dict is None:
            dict = {}
        if default is None:
            default = {}
        
        self.list = list(dict.values())
        self.default = default
        super().__init__(dict)

    def __getitem__(self, key: t.Any) -> t.Any:
        if key not in self or isinstance(key, (slice, int)):
            return self.list[key]
        return super().__getitem__(key)
    
    def get(self, key:'T', default=None) -> 'T|t.Literal[""]':
        if key in self:
            return self[key]
        elif default is not None:
            return default
        elif key in self.default:
            return self.default[key]
        else:
            return ""
    
CURSOR_STYLE = t.TypedDict("CURSOR_STYLE",
    {
        "bg-color": str,
        "fg-color": str,
    },
    total=False
)

SELECTED_STYLE = t.TypedDict("SELECTED_STYLE",
    {
        "bg-color": str,
        "fg-color": str,
    },
    total=False
)

DEBUG_STYLE = t.TypedDict("DEBUG_STYLE",
    {
        "bg-color": str,
        "fg-color": str,
    },
    total=False
)

STYLE = t.TypedDict("STYLE",
    {
        "cursor": CURSOR_STYLE,
        "selected": SELECTED_STYLE,
        "debugmode": bool,
        "debug": DEBUG_STYLE,
    },
    total=False
)


class Date:
    cache = Cache()
    months = Dict({'January':31, 'February':28, 'March':31, 'April':30, 'May':31, 'June':30, 'July':31, 'August':31, 'September':30, 'October':31, 'November':30, 'December':31})
    
    DEFAULT_STYLE:'STYLE' = {
        "cursor": {
            "bg-color": ANSIColors.bg_bright_cyan,
            "fg-color": ANSIColors.reset_fg,
        },
        "selected": {
            "bg-color": ANSIColors.bg_bright_green,
            "fg-color": ANSIColors.reset_fg,
        },
        "debugmode": False,
        "debug": {
            "bg-color": ANSIColors.bg_bright_red,
            "fg-color": ANSIColors.reset_fg,
        }
    }
    
    def __init__(self, style:'STYLE', min:'t.Union[d, None]'=None, max:'t.Union[d, None]'=None, default:'d'=None) -> None:
        self.style = Dict(style, default=self.DEFAULT_STYLE)
        self.min = min
        self.max = max
        self.default = default
        self.selected:'POS|t.Literal[False]' = False
        self._validator:'t.Callable[[list[d]], t.Union[str, t.Literal[True]]]' = lambda x: True
        self.error = ""
        logger.debug(f"Date.__init__: {self.style=} {self.min=} {self.max=} {self.default=}")

    def print(self):
        logger.debug("Date.print")
        screen = (
            f"{Cursor.clear_screen}"
            f"{f"<Q {self.pos.year} E>":^20}\n"
            f"{f"<q {self.months[self.pos.month-1]} e>":^20}\n"
            " M  T  W  T  F  S  S\n"
            "--------------------\n"
        )
        for row, week in enumerate(self.cache.get_or_add(self.pos.month, self.pos.year, self.get_days)):
            for col, day in enumerate(week):
                if self.pos.x == col and self.pos.y == row:
                    screen += f"{self.style['cursor']['bg-color']}{self.style['cursor']['fg-color']}{day.day:02d}{ANSIColors.reset} "
                elif self.selected and POS(col, row, self.pos.month, self.pos.year) < self.pos:
                    if POS(col, row, self.pos.month, self.pos.year) > self.selected:
                        screen += f"{self.style['selected']['bg-color']}{self.style['selected']['fg-color']}{day.day:02d} {ANSIColors.reset}"
                    elif self.style["debugmode"]:
                        screen += f"{self.style["debug"]["bg-color"]}{self.style['debug']['fg-color']}{day.day:02d} {ANSIColors.reset}"
                else:
                    screen += f"{day.day:02d} "
            screen += "\n"
        
        if self.error:
            screen += f"\n{self.error}"
        sys.stdout.write(screen)
        sys.stdout.flush()
        logger.debug("Date.print: Done")


        

    def handler(self, key):
        name = key.name
        logger.debug(f"Date.handler: {name=}")

        def chg_month(n):
            if n > 12:
                n = 1
                chg_year(self.pos.year+1)
            elif n < 1:
                n = 12
                chg_year(self.pos.year-1)
            self.pos.month = n

        def chg_year(n):
            self.pos.year = n

        def chg_day(n):
            def get_xy(n):
                for row, week in enumerate(self.cache.get_or_add(self.pos.month, self.pos.year, self.get_days)):
                    for col, day in enumerate(week):
                        if day.day == n:
                            return col, row
                return 0, 0
            
            if n > self.months[self.pos.month]:
                n = 1
                chg_month(self.pos.month+1)
            elif n < 1:
                n = self.months[self.pos.month]
                chg_month(self.pos.month-1)
            self.pos.xy = get_xy(n)

        if name in ["left", "a"]:
            chg_day(self.pos.day-1)
        elif name in ["right", "d"]:
            chg_day(self.pos.day+1)
        elif name in ["up", "w"]:
            chg_day(self.pos.day-7)
        elif name in ["down", "s"]:
            chg_day(self.pos.day+7)
        elif name == "enter":
            self.entered = True
        elif name == "space":
            self.selected = self.pos.copy()
        elif name == "shift+space":
            self.selected = False
        elif name == "q":
            chg_month(self.pos.month-1)
        elif name == "e":
            chg_month(self.pos.month+1)
        elif name == "Q":
            chg_year(self.pos.year-1)
        elif name == "E":
            chg_year(self.pos.year+1)
        elif name == "ctrl+c":
            raise KeyboardInterrupt
        else:
            return
        self.print()

    def run(self):
        logger.debug("Date.run")
        self.validated = False
        self.entered = False
        self.pos = POS(
            x=0,
            y=0,
            month=d.today().month,
            year=d.today().year
        )
        logger.debug("Date.run: Adding handler for keys")
        keyboard.on_press(self.handler, suppress=True)
        logger.debug("Date.run: Adding keyboard interrupt handler")
        def k_interupt(event):
            raise KeyboardInterrupt
        keyboard.add_hotkey("ctrl+c", k_interupt)
        logger.debug("Date.run: Printing screen")
        self.print()
        while not self.validated:
            while not self.entered:
                time.sleep(0.1)
            if self.selected == False:
                selected = []
            else:
                selected = self.pos.between(self.selected)
            self._validator(selected)

        logger.debug("Date.run: Done")

        return selected

        
    def validate(self):
        def wrapper(func):
            self._validator = func
            def inner():
                ret = func(self.selected)
                if isinstance(ret, str):
                    self.error = ret
                    self.selected = False
                else:
                    self.error = ""
                    self.validated = True
            return inner
        return wrapper

        

    def get_days(self, month:'int', year:'int') -> 'list[list[d]]':
        logger.debug(f"Date.get_days: Getting days for {month=} {year=}")
        min = d(year=year, month=month, day=1)
        day = min
        days:'list[d]' = []
        weeks:'list[list[d]]' = []
        ds = 0
        errors = False
        logger.debug(f"Date.get_days: {month=} {year=}")
        while errors==False and day.month == month:
            logger.debug(f"Date.get_days: Running loop for month")
            try:
                logger.debug(f"Date.get_days: Running loop for week {weeks=}")
                while ds != 7 and day.month == month:
                    logger.debug(f"Date.get_days: Adding day to week {ds=} {day=} {days=}")
                    days.append(day)
                    day += td(days=1)
                    ds += 1
                weeks.append(days)
                days = []
                ds = 0
            except OverflowError:
                errors = True
                break

        weeks.append(days)
        return weeks
