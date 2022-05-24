from typing import List, Dict

from src.compiler.allocator.types import ValueType


class SizeData:
    """Size data for a function, could also be used to keep track of global amount of each type,
     in recursion, could run out of max variables"""

    def __init__(self, int_count, float_count, bool_count, string_count):
        self.int_count = int_count
        self.float_count = float_count
        self.bool_count = bool_count
        self.string_count = string_count

    # TODO function to subtract variables once context memory is removed from stack
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
    """Data needed to run functions in virtual machine"""

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


class TypeData:
    """Type """

    def __init__(self, start, end, type_, segment):
        self.segment = segment
        self.type_ = type_
        self.start = start
        self.end = end


class Storage:
    """Exact storage for each type of variable"""

    def __init__(self, size: int):
        self.data = [None] * size
        self.pointer = 0
        self.size = size


class ContextMemory:
    """Memory stores exact amount of needed spaces for a specific function"""

    def __init__(self, size_data: SizeData, constant_data: "ContextMemory", global_data: "ContextMemory",
                 type_data: List[TypeData]):

        self.size_data = size_data
        self.type_data = type_data

        # TODO removed double mapping and use offset from known segment ranges
        self.data_storage: Dict[ValueType, any] = {}
        self.memory_map: Dict[int, int] = {}
        self.storage_map = Dict[ValueType, List]

        # Needed because these two are global
        self.global_data = global_data
        self.constant_data = constant_data

        self.__init_storage()

    def __init_storage(self):
        """Only for local variables"""
        self.data_storage[ValueType.INT] = Storage(self.size_data.int_count)
        self.data_storage[ValueType.FLOAT] = Storage(self.size_data.int_count)
        self.data_storage[ValueType.BOOL] = Storage(self.size_data.int_count)
        self.data_storage[ValueType.STRING] = Storage(self.size_data.int_count)

    def save(self, address, value):
        type_ = self.__decode_type(address)
        # check segment hash (Int, Float, etc..)
        segment: Storage = self.data_storage[type_]
        if address not in self.memory_map:
            # TODO calculate offset to know what index to place value in based on segment and type range
            segment.data[segment.pointer] = value
            self.memory_map[address] = segment.pointer
            segment.pointer += 1
            return

        index = self.memory_map[address]
        segment.data[index] = value

    def get(self, address):
        # TODO if segment is global, get from global, if from constant same thing, else from local
        type_ = self.__decode_type(address)
        segment: Storage = self.data_storage[type_]

        if address not in self.memory_map:
            return self.global_data.get(address)

        index = self.memory_map[address]
        return segment.data[index]

    # TODO decode segment

    def __decode_type(self, address: int):
        for type_data in self.type_data:
            if type_data.start <= address <= type_data.end:
                return type_data.type_

        return None
