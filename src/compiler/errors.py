class CompilerError:
    def __init__(self, message: str, location: str = "",  trace=""):
        self.message = message
        self.trace = trace
        self.location = location

    def print(self):
        print(f'Inside {self.trace}:{self.location} - CompilationError: {self.message}')
