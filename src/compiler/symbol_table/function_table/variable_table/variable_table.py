import math
from typing import Dict
from .variable import Variable, DimData
from src.compiler.stack_allocator.index import StackAllocator
from src.compiler.stack_allocator.helpers import Layers
from src.compiler.stack_allocator.types import ValueType
from src.utils.debug import Debug
from src.utils.display import make_table
from src.compiler.symbol_table.constant_table import ConstantTable


class VariableTable:
    def __init__(self):
        self.variables: Dict[str, Variable] = {}
        self.inverse_hash: Dict[int, any] = {}  # used to get dimensions
        self.current_variable = None

    def add(self, id_, is_param):
        """ Add Variable to `variables` dictionary if not existent """
        if self.variables.get(id_) is None:
            # we can't know where to put it without the type, just store the reference for now
            self.variables[id_] = Variable(id_, is_param=is_param)
            self.current_variable = self.variables[id_]
            return self.current_variable

    def add_dimension(self, size):
        """ Append new dimension `size` to current variable's `dimensions` list """
        dim_data = DimData(size=size)
        self.current_variable.dim_data_list.append(dim_data)

    def allocate_dimensions(self, layer: Layers, memory: StackAllocator, constant_table: ConstantTable):
        """ Multiply all the dimensions of current variable to allocate required space """

        dim_data_list = self.current_variable.dim_data_list

        # Calculate m for all dimensions except the rightmost
        for i in range(len(dim_data_list) - 1):
            sizes = [dim_data.size for dim_data in dim_data_list[i+1:]]
            m = math.prod(sizes)
            dim_data_list[i].m = m
            # Add m to constant table
            constant_table.add(m, memory)

        sizes = [dim_data.size for dim_data in dim_data_list]
        size = math.prod(sizes)

        return size

    def set_type(self, type_, layer: Layers, memory: StackAllocator, class_id):
        """ Sets current var type """
        enum_value = ValueType(type_)
        address = memory.allocate_address(enum_value, layer)

        Debug.map()[address] = str(self.current_variable.id_)
        self.current_variable.type_ = enum_value
        self.current_variable.class_id = class_id
        self.current_variable.address_ = address
        self.inverse_hash[address] = self.current_variable

        return self.current_variable.id_

    def get_from_address(self, address):
        if self.inverse_hash.get(address) is None:
            return None

        return self.inverse_hash[address]

    def display(self, id_):
        print(make_table(id_ + ": Variables", ["ID", "TYPE", "ADDRESS"],
                         map(lambda fun: [fun[0], fun[1].type_.value, fun[1].address_], self.variables.items())))
