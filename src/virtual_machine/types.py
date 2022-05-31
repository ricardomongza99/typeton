from typing import Dict, List

from src.compiler.allocator.helpers import Layers, init_types, get_segment, get_resource, Segment
from src.compiler.allocator.types import ValueType, DEFAULT_TYPES, TypeRange
from src.compiler.symbol_table.constant_table import ConstantTable


class SizeUnit:
    """Used to store the variable count for each type inside a function"""

    def __init__(self):
        self.local = 0
        self.temp = 0

    @property
    def total(self):
        return self.local + self.temp


class SizeData:
    """Size data for a function, could also be used to keep track of global amount of each type,
     in recursion, could run out of max variables"""

    def __init__(self):
        # Store in hash for easy access
        self.hash: Dict[str, SizeUnit] = {
            ValueType.INT.value: SizeUnit(),
            ValueType.FLOAT.value: SizeUnit(),
            ValueType.BOOL.value: SizeUnit(),
            ValueType.STRING.value: SizeUnit()}

    def get_data(self, type_: ValueType):
        return self.hash[type_.value]

    # TODO function to subtract variables once context memory is removed from stack, or maybe make another class
    def add_variable_size(self, type_: ValueType, segment: Layers):
        if segment is Layers.TEMPORARY:
            self.hash[type_.value].temp += 1
        else:
            self.hash[type_.value].local += 1

    def display(self):
        print("Size Data:")
        ints = self.hash[ValueType.INT.value]
        floats = self.hash[ValueType.FLOAT.value]
        strings = self.hash[ValueType.STRING.value]
        bools = self.hash[ValueType.BOOL.value]

        print("Ints", "local", ints.local, "temp", ints.temp)
        print("String", "local", strings.local, "temp", strings.temp)
        print("Float", "local", floats.local, "temp", floats.temp)
        print("Bools", "local", bools.local, "temp", bools.temp)


class FunctionData:
    """Data needed to run functions in virtual machine"""

    def __init__(self, id_: str, start_quad: int = 0):
        self.id_ = id_
        self.size_data = SizeData()
        self.start_quad = start_quad
        self.type_ = None
        self.parameter_signature = []

    def add_variable_size(self, type_: ValueType, segment: Layers):
        self.size_data.add_variable_size(type_, segment)

    def print_signature(self):
        result = ""
        for type_ in self.parameter_signature:
            result += f'{type_.value}:'

        if result == "":
            return "No Params"
        return result[:-1]


def init_storage(size):
    return [None] * size


class ContextMemory:
    """Memory stores exact amount of needed spaces for a specific function"""

    # TODO move size_data init_types to outside of ContextMemory

    def __init__(self, size_data: SizeData, constant_data: ConstantTable,
                 global_data):
        self.pending_return_value = None
        self.type_data = init_types(DEFAULT_TYPES, is_runtime=True)
        self.size_data = size_data

        # TODO removed double mapping and use offset from known segment ranges
        self.data_storage: Dict[ValueType, List] = {}

        # Needed because these two are global
        self.global_data = global_data
        self.constant_data = constant_data

        self.__init_storage()

    def display(self):
        print("Ints", self.data_storage[ValueType.INT])
        print("Float", self.data_storage[ValueType.FLOAT])
        print("Bool", self.data_storage[ValueType.BOOL])
        print("String", self.data_storage[ValueType.STRING])

    def get_type(self, address):
        segment = get_segment(address, self.type_data)
        type_data: TypeRange = get_resource(address, segment)
        return type_data.type_

    def __init_storage(self):
        """Only for local variables"""
        self.data_storage[ValueType.INT] = init_storage(self.size_data.get_data(ValueType.INT).total)
        self.data_storage[ValueType.FLOAT] = init_storage(self.size_data.get_data(ValueType.FLOAT).total)
        self.data_storage[ValueType.BOOL] = init_storage(self.size_data.get_data(ValueType.BOOL).total)
        self.data_storage[ValueType.STRING] = init_storage(self.size_data.get_data(ValueType.STRING).total)

    def get_offset(self, address, segment: Segment, type_data: TypeRange):
        """Get offset based on address segment range to store in exact array"""
        offset = address - type_data.start
        if segment.type_ is Layers.TEMPORARY:
            offset += self.size_data.get_data(type_data.type_).local
        return offset

    def is_global(self):
        return self.global_data == None

    def __save_global(self, address, value):
        if self.global_data is None:
            self.global_data.save(address, value)

    def save(self, address, value):
        """Deduce type and store in corresponding array slot"""
        segment = get_segment(address, self.type_data)
        type_data: TypeRange = get_resource(address, segment)

        if segment.type_ is Layers.GLOBAL and not self.is_global():
            self.global_data.save(address, value)
            return

        if segment.type_ is Layers.CONSTANT:
            return

        slot = self.data_storage[type_data.type_]
        offset = self.get_offset(address, segment, type_data)
        slot[offset] = value

    def map_parameter(self, argument_value, argument_address, parameter_index):
        """Map parameters from previous context to current local context"""
        segment = get_segment(argument_address, self.type_data)
        type_data: TypeRange = get_resource(argument_address, segment)

        slot = self.data_storage[type_data.type_]
        slot[parameter_index] = argument_value

    def get(self, address):
        """Get from address origin, be it global, local, or constant table"""
        segment = get_segment(address, self.type_data)
        type_data: TypeRange = get_resource(address, segment)
        if segment.type_ is Layers.GLOBAL and not self.is_global():
            return self.global_data.get(address)

        if segment.type_ is Layers.CONSTANT:
            const = self.constant_data.get_from_address(f'{address}')
            return const

        # else get from local memory
        slot = self.data_storage[type_data.type_]
        offset = self.get_offset(address, segment, type_data)
        return slot[offset]
