from typing import Dict

from src.utils.debug import Debug
from src.utils.display import make_table
from src.allocator.allocator import Allocator
from src.allocator.helpers import Layers
from src.allocator.types import ValueType


class Constant:
    def __init__(self, address, type_):
        self.address = address
        self.type_ = type_


class ConstantTable:
    def __init__(self):
        self.table: Dict[str, Constant] = {}

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

        address, error = memory.allocate_address(type_, Layers.CONSTANT)

        debug = Debug.get_instance().map()
        debug[address] = str(value)
        if error:  # TODO error handling
            return
        self.table[value] = Constant(address, type_)
        return address

    def get(self, value):
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
