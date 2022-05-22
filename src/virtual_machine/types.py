from typing import List, Dict

from src.utils.display import make_table
from src.virtual.types import ValueType


class SizeData:
    def __init__(self, int_count, float_count, bool_count, string_count):
        self.int_count = int_count
        self.float_count = float_count
        self.bool_count = bool_count
        self.string_count = string_count

    def add_variable_size(self, type_: ValueType):
        if type_ is ValueType.INT:
            self.int_count += 1
        elif type_ is ValueType.FLOAT:
            self.float_count += 1
        elif type_ is ValueType.BOOL:
            self.bool_count += 1
        elif type_ is ValueType.STRING:
            self.string_count += 1
        else:
            print("Error unknown type")


class FunctionData:
    def __init__(self, id_: str, start_quad: int = 0):
        self.id_ = id_
        self.size_data = SizeData(0, 0, 0, 0)
        self.start_quad = start_quad
        self.type_ = None
        self.parameter_signature = []

    def add_variable_size(self, type_: ValueType):
        self.size_data.add_variable_size(type_)

    def print_signature(self):
        result = ""
        for type_ in self.parameter_signature:
            result += f'{type_.value}:'

        if result == "":
            return "No Params"
        return result[:-1]



class Directory:
    def __init__(self, function_list: List[FunctionData]):
        self.function_list = function_list


class TypeData:
    def __init__(self, start, end, type_):
        self.type_ = type_
        self.start = start
        self.end = end


class Storage:
    def __init__(self, size: int):
        self.data = [None] * size
        self.pointer = 0
        self.size = size


class ContextMemory:
    def __init__(self, size_data: SizeData, global_data: "ContextMemory", type_data: List[TypeData]):
        self.size_data = size_data
        self.global_data = global_data
        self.type_data = type_data
        self.data_storage: Dict[ValueType, any] = {}
        self.memory_map: Dict[int, int] = {}
        self.storage_map = Dict[ValueType, List]
        self.__init_storage()

    def __init_storage(self):
        self.data_storage[ValueType.INT] = Storage(self.size_data.int_count)
        self.data_storage[ValueType.FLOAT] = Storage(self.size_data.int_count)
        self.data_storage[ValueType.BOOL] = Storage(self.size_data.int_count)
        self.data_storage[ValueType.STRING] = Storage(self.size_data.int_count)

    def save(self, address, value):
        type_ = self.__decode_type(address)
        segment: Storage = self.data_storage[type_]
        if address not in self.memory_map:
            segment.data[segment.pointer] = value
            self.memory_map[address] = segment.pointer
            segment.pointer += 1
            return

        index = self.memory_map[address]
        segment.data[index] = value

    def get(self, address):
        type_ = self.__decode_type(address)
        segment: Storage = self.data_storage[type_]

        if address not in self.memory_map:
            return self.global_data.get(address)

        index = self.memory_map[address]
        return segment.data[index]

    def __decode_type(self, address: int):
        for type_data in self.type_data:
            if type_data.start <= address <= type_data.end:
                return type_data.type_

        return None
