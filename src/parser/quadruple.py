from enum import Enum


class OperationType(Enum):
    MULTIPLY = '*'
    DIVIDE = '/'
    ADD = '+'
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


class Quadruple:
    def __init__(self, operation, left_address, right_address, result_address):
        self.operation: OperationType = OperationType(operation)
        self.left_address = left_address
        self.right_address = right_address
        self.result_address = result_address
