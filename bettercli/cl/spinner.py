import sys
import time
import typing as t
from threading import Thread


_T_contra = t.TypeVar("_T_contra", contravariant=True)

class SupportsFlush(t.Protocol):
    def flush(self) -> object: ...

class SupportsWrite(t.Protocol[_T_contra]):
    def write(self, s: _T_contra, /) -> object: ...


Message = t.TypedDict("Message", {
    "fg-color": str,
    "bg-color": str,
    "message": t.Required[str],
}, total=False)

State = t.TypedDict("State", {
    "fg-color": str,
    "bg-color": str,
    "symbol": str,
    "wait": float,
    "message": Message,
}, total=False)

Style = t.TypedDict("Style", {
    "bg-color": str,
    "fg-color": str,
    "states": list[State],
    "wait": float,
    "messages": dict[t.Union[float, int], Message],

}, total=False)

class Spinner:
    """A terminal spinner animation."""
    
    def __init__(self, style: Style = None) -> None:
        self.style = style
        self._running: 'bool' = False
        self._print: 'list[tuple]' = []
        self.thread: 't.Optional[Thread]' = None
        self.message: 'str' = ""
        if self.style is None:
            self.style = {
                "states": [
                    {"symbol": "⠋", "wait": 0.1},
                    {"symbol": "⠙", "wait": 0.1},
                    {"symbol": "⠹", "wait": 0.1},
                    {"symbol": "⠸", "wait": 0.1},
                    {"symbol": "⠼", "wait": 0.1},
                    {"symbol": "⠴", "wait": 0.1},
                    {"symbol": "⠦", "wait": 0.1},
                    {"symbol": "⠧", "wait": 0.1},
                    {"symbol": "⠇", "wait": 0.1},
                ]
            }
        elif "states" in self.style:
            for state in self.style["states"]:
                if "wait" not in state:
                    state["wait"] = self.style.get("wait", 0.1)
        else:
            self.style.update({
                "states": [
                    {"symbol": "⠋", "wait": 0.1},
                    {"symbol": "⠙", "wait": 0.1},
                    {"symbol": "⠹", "wait": 0.1},
                    {"symbol": "⠸", "wait": 0.1},
                    {"symbol": "⠼", "wait": 0.1},
                    {"symbol": "⠴", "wait": 0.1},
                    {"symbol": "⠦", "wait": 0.1},
                    {"symbol": "⠧", "wait": 0.1},
                    {"symbol": "⠇", "wait": 0.1},
                ]
            })

    def run(self) -> None:
        """Start the spinner animation in a separate thread."""
        self._running = True
        self.thread = Thread(target=self._spin, args=(sys.stdout,))
        self.thread.daemon = True  # Allow the program to exit if thread is still running
        self.thread.start()

    def stop(self) -> None:
        """Stop the spinner animation."""
        self._running = False
        if self.thread:
            self.thread.join()
        print('\r' + ' ' * 20 + '\r', end='')  # Clear the spinner line
        sys.stdout.flush()

    def _spin(self, stream: 't.TextIO') -> None:
        """Run the spinner animation."""
        while self._running:
            for state in self.style["states"]:
                while self._print:
                    values, sep, end, flush = self._print.pop(0)
                    print("\r", *values, sep=sep, end=end, file=stream, flush=flush)
                    stream.flush()

                if not self._running:
                    break
                symbol = state["symbol"]
                wait = state["wait"]

                if "fg-color" in state:
                    symbol = f"\033[{state['fg-color']}m{symbol}\033[0m"
                if "bg-color" in state:
                    symbol = f"\033[{state['bg-color']}m{symbol}\033[0m"

                message = self.message or self._format_message(state.get("message", {"message": ""}))

                print(f"\r{symbol} {message}", end='', file=stream)
                stream.flush()
                time.sleep(wait)

    def _format_message(self, message: 'Message'):
        msg = message["message"]
        if "fg-color" in message:
            msg = f"\033[{message['fg-color']}m{msg}\033[0m"
        if "bg-color" in message:
            msg = f"\033[{message['bg-color']}m{msg}\033[0m"
        return msg

    def set_message(self, message: 'Message', duration: 'float' = -1):
        """
        Args:
            message (str): The message to display.
            duration (float, optional): The duration of the message in seconds. Set to -1 to keep the message indefinitely. Defaults to -1.
        """        
        def _sleep(spinner: 'Spinner', duration: 'float'):
            time.sleep(duration)
            spinner.message = ""

        self.message = self._format_message(message)
        if duration > 0:
            thread = Thread(target=_sleep, args=(self, duration))
            thread.start()

    def __enter__(self) -> 'Spinner':
        """Context manager entry."""
        self.run()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.stop()

    @t.overload
    def print(
        *values: 'object',
        sep: 'str | None' = " ",
        end: 'str | None' = "\n",
        flush: 't.Literal[False]' = False,
    ) -> 'None': ...
    @t.overload
    def print(
        *values: 'object', sep: 'str | None' = " ", end: 'str | None' = "\n", flush: 'bool'
    ) -> 'None': ...

    def print(self, *values, sep=' ', end='\n', flush=False):
        self._print.append((values, sep, end, flush))