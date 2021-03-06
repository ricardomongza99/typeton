from typing import Dict

import jsonpickle
from src.compiler.errors import CompilerError, CompilerEvent

from src.compiler.stack_allocator.index import StackAllocator
from src.compiler.stack_allocator.helpers import Layers
from src.compiler.stack_allocator.types import ValueType
from src.utils.debug import Debug
from src.utils.display import make_table
from src.utils.observer import Event, Publisher
from .constant import Constant


class ConstantTable(Publisher):
    def __init__(self):
        super().__init__()
        self.constants: Dict[str, Constant] = {}
        self.inverse_hash: Dict[int, any] = {}

    def add(self, value, memory: StackAllocator):
        if self.exists(value):
            return

        if type(value) is int:
            type_ = ValueType.INT
        elif type(value) is float:
            type_ = ValueType.FLOAT
        elif value == 'true' or value == 'false':
            type_ = ValueType.BOOL
        elif type(value) is str:
            type_ = ValueType.STRING
        else:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError(
                f'Unsupported type {type(value)}')))

        address = memory.allocate_address(type_, Layers.CONSTANT)

        debug = Debug.get_instance().map()
        debug[address] = str(value)

        self.constants[value] = Constant(address, type_)
        self.inverse_hash[address] = value
        return address

    def get_from_address(self, address):
        if self.inverse_hash.get(address) is None:
            self.broadcast(Event(CompilerEvent.STOP_COMPILE, CompilerError(
                f'Address {address} does not exist')))

        return self.inverse_hash[address]

    def get_from_value(self, value):
        if self.constants.get(value) is None:
            return

        return self.constants[value]

    def display(self):
        print(make_table("Constants", ["ID", "TYPE", "ADRESS"],
                         map(lambda fun: [fun[0], fun[1].type_.value, fun[1].address], self.constants.items())))

    def exists(self, key):
        if self.constants.get(key) is None:
            return False
        return True

    def get_output_values_dict(self):
        """ Returns { address: value } dictionary used by the output file"""
        return jsonpickle.encode(self, keys=True)
