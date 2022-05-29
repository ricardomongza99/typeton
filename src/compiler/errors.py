from enum import Enum

from src.utils.observer import Subscriber, Publisher, Event


class CompilerError:
    def __init__(self, message: str, location: str = "", trace=""):
        self.message = message
        self.trace = trace
        self.location = location

    def print(self):
        print(f'Inside {self.trace}:{self.location} - CompilationError: {self.message}')


class CompilerEvent(Enum):
    STOP_COMPILE = 0
    GEN_END_FUNC = 1
    FREE_MEMORY = 2
    GO_TO_MAIN = 3


