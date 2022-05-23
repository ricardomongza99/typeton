from typing import Dict

from .variable import Variable
from ..parser.errors import CompilerError
from ..singleton.debug import Debug
from ..utils.display import make_table
from ..allocator.index import Scheduler
from ..allocator.helpers import Layers
from ..allocator.types import ValueType


class VariableTable:
    def __init__(self):
        self.variables: Dict[str, Variable] = {}
        self.current_id = None

    @property
    def current_variable(self):
        return self.variables[self.current_id]

    def add(self, id_, is_param):
        """ Add Variable to `variables` dictionary if not existent """
        if self.variables.get(id_) is None:
            self.current_id = id_
            # we can't know where to put it without the type, just store the reference for now
            self.variables[id_] = Variable(is_param=is_param)

    def set_type(self, type_, layer: Layers, memory: Scheduler):
        """ Sets current var type """
        enum_value = ValueType(type_)
        address, error = memory.schedule_address(enum_value, layer)
        if error:  # TODO Create class to create compilation errors
            Debug.add_error(CompilerError("Too many Variables"))

        debug: Debug = Debug.get_instance().get_map()
        debug[address] = str(self.current_id)
        self.current_variable.type_ = enum_value
        self.current_variable.address_ = address

        return self.current_id

    def display(self, id_):
        return make_table(id_ + ": Variables", ["ID", "TYPE", "ADDRESS"],
                          map(lambda fun: [fun[0], fun[1].type_.value, fun[1].address_], self.variables.items()))
