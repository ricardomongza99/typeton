from audioop import add
from enum import Enum
from src.utils.observer import Event, Publisher
from typing import Dict, List

from src.compiler.stack_allocator.helpers import Layers, init_types, get_segment, get_resource, Segment
from src.compiler.stack_allocator.types import ValueType, DEFAULT_TYPES, TypeRange
from src.compiler.symbol_table.constant_table import ConstantTable
from src.config.definitions import HEAP_RANGE_SIZE
from src.virtual_machine.heap_memory import Heap


class PointerAction(Enum):
    REFERENCE = 'reference'
    VALUE = 'value'


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
            ValueType.STRING.value: SizeUnit(),
            ValueType.POINTER.value: SizeUnit()
        }

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

# TODO get heap start


class ContextMemory(Publisher):
    """Memory stores exact amount of needed spaces for a specific function"""

    # TODO move size_data init_types to outside of ContextMemory

    def __init__(self, size_data: SizeData, constant_data: ConstantTable,
                 global_data, object_heap: Heap):
        self.pending_return_value = None
        self.type_data = init_types(DEFAULT_TYPES, is_runtime=True)
        self.size_data = size_data
        self.object_heap = object_heap
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
        _, address = pure_address(address)
        segment = get_segment(address, self.type_data)
        type_data: TypeRange = get_resource(address, segment)
        return type_data.type_

    def __init_storage(self):
        self.data_storage[ValueType.INT] = init_storage(self.size_data.get_data(ValueType.INT).total)
        self.data_storage[ValueType.FLOAT] = init_storage(self.size_data.get_data(ValueType.FLOAT).total)
        self.data_storage[ValueType.BOOL] = init_storage(self.size_data.get_data(ValueType.BOOL).total)
        self.data_storage[ValueType.STRING] = init_storage(self.size_data.get_data(ValueType.STRING).total)
        self.data_storage[ValueType.POINTER] = init_storage(self.size_data.get_data(ValueType.POINTER).total)

    def get_offset(self, address, segment: Segment, type_data: TypeRange):
        """Get offset based on address segment range to store in exact array"""
        offset = address - type_data.start
        if segment.type_ is Layers.TEMPORARY:
            offset += self.size_data.get_data(type_data.type_).local

        return offset

    def is_global(self):
        return self.global_data == None

    def release_reference(self, address):
        """Release reference to object"""
        # print('starting release of memory ')
        self.object_heap.release_heap_memory(self.get(f'&{address}'))
        # print('finished release of memory ')

    def save_reference(self, address, value):
        """Save value to pointer"""

        # print("saving to pointer address", address, value)

        segment = get_segment(address, self.type_data)

        if segment.type_ is Layers.GLOBAL and not self.is_global():
            return self.global_data.save_reference(address, value)

        type_data: TypeRange = get_resource(address, segment)
        slot = self.data_storage[type_data.type_]
        offset = self.get_offset(address, segment, type_data)

        slot[offset] = value

    def save(self, address, value):
        """Deduce type and store in corresponding array slot"""
        action, pure_addr = pure_address(address)

        segment = get_segment(pure_addr, self.type_data)
        type_data: TypeRange = get_resource(pure_addr, segment)

        if segment.type_ is Layers.GLOBAL and not self.is_global():
            self.global_data.save(address, value)
            return

        slot = self.data_storage[type_data.type_]
        offset = self.get_offset(pure_addr, segment, type_data)

        if type_data.type_ is ValueType.POINTER:
            if action is PointerAction.REFERENCE:
                slot[offset] = value
                return
            elif action is PointerAction.VALUE or action is None:
                # print('saving value from pointer', address,
                #       "actual address", slot[offset], 'for value', value)
                self.object_heap.set_value(slot[offset], value)
                return

        slot[offset] = value

    def map_parameter(self, argument_value, argument_address, parameter_index):
        """Map parameters from previous context to current local context"""
        segment = get_segment(argument_address, self.type_data)
        type_data: TypeRange = get_resource(argument_address, segment)

        slot = self.data_storage[type_data.type_]
        slot[parameter_index] = argument_value

    def get(self, address):
        """Get from address origin, be it global, local, or constant table"""
        action, pure_addr = pure_address(address)

        segment = get_segment(pure_addr, self.type_data)
        type_data: TypeRange = get_resource(pure_addr, segment)

        if segment.type_ is Layers.GLOBAL and not self.is_global():
            return self.global_data.get(address)

        if segment.type_ is Layers.CONSTANT:
            const = self.constant_data.get_from_address(f'{pure_addr}')
            return const

        # else get from local memory
        slot = self.data_storage[type_data.type_]
        offset = self.get_offset(pure_addr, segment, type_data)

        if type_data.type_ is ValueType.POINTER:
            # print("getting pointer", address, slot[offset])
            if action is PointerAction.REFERENCE:
                return slot[offset]
            else:
                return self.object_heap.get_value(slot[offset])

        return slot[offset]


def pointer_type(address):
    # return pointer type using enum by checking if the first char is a '&' or a '*'
    if address[0] == '&':
        return PointerAction.REFERENCE, int(address[1:])
    elif address[0] == '*':
        return PointerAction.VALUE, int(address[1:])


def pure_address(address):
    if type(address) is int:
        return None, address
    # return pure address without pointer type
    elif address[0] == '&':
        return PointerAction.REFERENCE, int(address[1:])
    elif address[0] == '*':
        return PointerAction.VALUE, int(address[1:])
