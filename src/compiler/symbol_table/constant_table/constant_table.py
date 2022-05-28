from typing import Dict

import jsonpickle

from src.compiler.allocator.allocator import Allocator
from src.compiler.allocator.helpers import Layers
from src.compiler.allocator.types import ValueType
from src.utils.debug import Debug
from src.utils.display import make_table
from .constant import Constant


class ConstantTable:
    def __init__(self):
        self.table: Dict[str, Constant] = {}
        self.inverse_hash: Dict[int, any] = {}

    def add(self, value, memory: Allocator):
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
            print(value, 'doesnt exit')
            # TODO error handling
            return

        address = memory.allocate_address(type_, Layers.CONSTANT)

        debug = Debug.get_instance().map()
        debug[address] = str(value)

        self.table[value] = Constant(address, type_)
        self.inverse_hash[address] = value
        return address

    def get_from_address(self, address):
        if self.inverse_hash.get(address) is None:
            # TODO error handling
            return

        return self.inverse_hash[address]

    def get_from_value(self, value):
        if self.table.get(value) is None:
            # TODO error handling
            return

        return self.table[value]

    def display(self):
        print(make_table("Constants", ["ID", "TYPE", "ADRESS"],
                         map(lambda fun: [fun[0], fun[1].type_.value, fun[1].address], self.table.items())))

    def exists(self, key):
        if self.table.get(key) is None:
            return False
        return True

    def get_output_values_dict(self):
        """ Returns { address: value } dictionary used by the output file"""
        return jsonpickle.encode(self, keys=True)
