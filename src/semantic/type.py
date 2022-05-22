from src.parser.errors import CompilerError
from src.semantic.quadruple import Quad, OperationType
from src.virtual.types import ValueType


class ActionResult:
    def __init__(self, quad: Quad = None, error: CompilerError = None):
        self.quad = quad
        self.error = error

    def has_error(self):
        return self.error is not None

    def has_quad(self):
        return self.quad is not None


class Operator:
    def __init__(self, priority: int, type_: OperationType):
        self.priority = priority
        self.type_ = type_


class Operand:
    def __init__(self, type_: ValueType, address: int):
        self.type_ = type_
        self.address = address