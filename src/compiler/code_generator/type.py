from enum import Enum

from src.compiler.allocator.types import ValueType


class OperationType(Enum):
    CALL_ASSIGN = 'callassign'
    PARAM = 'param'
    ARE = 'are'
    GOTOMAIN = 'gotomain'
    MULTIPLY = '*'
    DIVIDE = '/'
    ADD = '+'
    EQUAL = '=='
    AND = '&&'
    OR = '||'
    LESS_THAN = '<'
    GREAT_THAN = '>'
    LESS_EQUAL = '<='
    GREAT_EQUAL = '>='
    LPAREN = '('
    RPAREN = ')'
    SUBTRACT = '-'
    ASSIGN = '='
    GOTOF = 'gotof'
    GOTOV = 'gotov'
    GOTO = 'goto'
    PARAMETER = 'parameter'
    RETURN = 'return'
    GOSUB = 'gosub'
    ENDFUNC = 'endfunc'
    ERA = 'era'
    END = 'end'
    PRINT = 'print'
    VERIFY = 'verify'


class Operator:
    def __init__(self, priority: int, type_: OperationType):
        self.priority = priority
        self.type_ = type_


class Operand:
    def __init__(self, type_: ValueType, address: int):
        self.type_ = type_
        self.address = address


class Quad:
    def __init__(self, operation, left_address=None, right_address=None, result_address=None):
        self.operation: OperationType = OperationType(operation)
        self.left_address = left_address
        self.right_address = right_address
        self.result_address = result_address

    def display(self, index):
        # unwrap None values
        left_address = '----' if self.left_address is None else self.left_address
        right_address = '----' if self.right_address is None else self.right_address

        print('{:3}. {:<5} {:<5} {:<5} {:<5}'.format(index,
                                                     self.operation.value,
                                                     left_address,
                                                     right_address,
                                                     self.result_address))
