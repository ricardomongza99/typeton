from enum import Enum
from queue import Queue
from src.config.definitions import INT_RANGE_SIZE, FLOAT_RANGE_SIZE, BOOL_RANGE_SIZE, STRING_RANGE_SIZE


class ValueType(Enum):
    INT = "Int"
    VOID = "Void"
    STRING = "String"
    FLOAT = "Float"
    BOOL = "Bool"


class TypeResource:
    def __init__(self, start, end, resource_type: ValueType):
        self.type = resource_type
        self.start = start
        self.end = end
        self.pointer = start
        self.free_addresses_list = Queue()


class MemoryType:
    def __init__(self, value_type: ValueType, size: int):
        self.type = value_type
        self.size = size


DEFAULT_TYPES = [
    MemoryType(value_type=ValueType.INT, size=INT_RANGE_SIZE),
    MemoryType(value_type=ValueType.FLOAT, size=FLOAT_RANGE_SIZE),
    MemoryType(value_type=ValueType.BOOL, size=BOOL_RANGE_SIZE),
    MemoryType(value_type=ValueType.STRING, size=STRING_RANGE_SIZE)
]
