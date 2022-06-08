from enum import Enum

from src.compiler.stack_allocator.types import ValueType


class OperationType(Enum):
    ALLOCATE_HEAP = 'allocateheap'
    END_GLOBAL = 'endglobal'
    ARRAY_ADD = 'arrayadd'
    DELETE_REF = 'deleteref'
    CALL_ASSIGN = 'callassign'
    POINTER_ADD = 'pointeradd'
    PARAM = 'param'
    ARE = 'are'
    GOTOMAIN = 'gotomain'
    MULTIPLY = '*'
    DIVIDE = '/'
    ADD = '+'
    EQUAL = '=='
    AND = '&&'
    OR = '||'
    NOT_EQUAL = '!='
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
    LASSIGN = '-='
    PASSIGN = '+='
    DASSIGN = '/='
    MASSIGN = '*='
    POINTER_ASSIGN = '&='
    VERIFY = 'verify'
    INPUT = 'input'


class FunctionTableEvents(Enum):
    ADD_TEMP = 0


class Operator:
    def __init__(self, priority: int, type_: OperationType):
        self.priority = priority
        self.type_ = type_


class Dimension:
    def __init__(self, size_address, m_address=None):
        self.size_address = size_address
        self.m_address = m_address


class Operand:
    def __init__(self, type_: ValueType, address: int, class_id=None, is_class_param=False):
        self.type_ = type_
        self.address = address
        self.class_id = class_id
        self.is_class_param = is_class_param


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
                                                     self.operation.value if self.operation is not None else '',
                                                     left_address if self.left_address is not None else '',
                                                     right_address if self.right_address is not None else '',
                                                     self.result_address if self.result_address is not None else ''))
