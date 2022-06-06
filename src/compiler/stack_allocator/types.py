from ctypes import pointer
from enum import Enum
from queue import Queue
from src.config.definitions import INT_RANGE_SIZE, FLOAT_RANGE_SIZE, BOOL_RANGE_SIZE, POINTER_RANGE_SIZE, STRING_RANGE_SIZE


class ValueType(Enum):
    INT = "Int"
    VOID = "Void"
    STRING = "String"
    FLOAT = "Float"
    BOOL = "Bool"
    POINTER = "Pointer"


class TypeRange:
    def __init__(self, start, end, resource_type: ValueType):
        self.type_ = resource_type
        self.start = start
        self.end = end


class TypeResource(TypeRange):
    def __init__(self, start, end, resource_type: ValueType):
        self.start = start
        super().__init__(start, end, resource_type)
        self.free_addresses_list = Queue()
        self.pointer = start

    def reset(self):
        self.pointer = self.start


class MemoryType:
    def __init__(self, value_type: ValueType, size: int):
        self.type = value_type
        self.size = size


DEFAULT_TYPES = [
    MemoryType(value_type=ValueType.INT, size=INT_RANGE_SIZE),
    MemoryType(value_type=ValueType.FLOAT, size=FLOAT_RANGE_SIZE),
    MemoryType(value_type=ValueType.BOOL, size=BOOL_RANGE_SIZE),
    MemoryType(value_type=ValueType.STRING, size=STRING_RANGE_SIZE),
    MemoryType(value_type=ValueType.POINTER, size=POINTER_RANGE_SIZE)
]
