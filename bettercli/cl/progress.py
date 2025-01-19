import typing as t
import time

STYLE = t.TypedDict("STYLE", {"bg-color": str, "fg-color": str, "symbol": str, "width": int, "height": int}, total=False)

PROGRESS = """
------------
|
"""

class Progress:
    def __init__(self, total:'int', style:'STYLE'):
        self.total = total
        self.style = style
        self.progress = 0
        self.tasks = {}

    def add_task(self, callback:'t.Callable[[], None]', when:'int'):
        self.tasks[when].append(callback)

    def task(self, when:'int'):
        def decorator(func):
            self.add_task(func, when)
            return func
        return decorator
    
    def run(self, total:'int'=100):
        """
        Args:
            total (int, optional): The total number of seconds to run the progress bar for. Defaults to 100.
        """
        step = total/0.02
        while not self.finished:
            self.update(step)
            time.sleep(0.02)

    @property
    def finished(self):
        return self.progress >= self.total
    
    def update(self, advance:'float'=1):
        self.progress += advance
        self.progress = min(self.progress, self.total)
        self.print()

    def print(self):
        raise NotImplementedError("print must be implemented by subclasses")
    
class Rectangle(Progress):
    def print(self):
        print("""
┏━━━━━━━━━━━━┓
┃           ┃
┗━━━━━━━━━━━━┛

""")

    

p=ProgressBar(100)

@p.task(0)
def task1():
    print("task1")

