from src.parser.errors import CompilerError
from src.semantic.quadruple import Quad


class ActionResult:
    def __init__(self, quad: Quad = None, error: CompilerError = None):
        self.quad = quad
        self.error = error

    def has_error(self):
        return self.error is not None

    def has_quad(self):
        return self.quad is not None

