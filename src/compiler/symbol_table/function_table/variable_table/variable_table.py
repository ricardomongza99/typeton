import math
from typing import Dict
from .variable import Variable
from src.compiler.allocator.allocator import Allocator
from src.compiler.allocator.helpers import Layers
from src.compiler.allocator.types import ValueType
from src.utils.debug import Debug
from src.utils.display import make_table


class VariableTable:
    def __init__(self):
        self.variables: Dict[str, Variable] = {}
        self.current_variable = None

    def add(self, id_, is_param):
        """ Add Variable to `variables` dictionary if not existent """
        if self.variables.get(id_) is None:
            # we can't know where to put it without the type, just store the reference for now
            self.variables[id_] = Variable(id_, is_param=is_param)
            self.current_variable = self.variables[id_]

    def add_dimension(self, size):
        """ Append new dimension `size` to current variable's `dimensions` list """
        self.current_variable.dimensions.append(size)

    def allocate_dimensions(self, layer: Layers, memory: Allocator):
        """ Multiply all the dimensions of current variable to allocate required space """
        size = math.prod(self.current_variable.dimensions)
        memory.allocate_space(self.current_variable.type_, layer, size)

    def set_type(self, type_, layer: Layers, memory: Allocator):
        """ Sets current var type """
        enum_value = ValueType(type_)
        address = memory.allocate_address(enum_value, layer)

        Debug.map()[address] = str(self.current_variable.id_)
        self.current_variable.type_ = enum_value
        self.current_variable.address_ = address

        return self.current_variable.id_

    def display(self, id_):
        print(make_table(id_ + ": Variables", ["ID", "TYPE", "ADDRESS"],
                         map(lambda fun: [fun[0], fun[1].type_.value, fun[1].address_], self.variables.items())))
