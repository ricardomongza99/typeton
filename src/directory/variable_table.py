from typing import Dict

from .variable import Variable
from ..virtual.compilation import Scheduler
from ..virtual.types import ValueType


class VariableTable:
    def __init__(self):
        self.variables: Dict[str, Variable] = {}
        self.current_id = None

    @property
    def current_variable(self):
        return self.variables[self.current_id]

    def add(self, id_):
        """ Add Variable to `variables` dictionary if not existent """
        if self.variables.get(id_) is None:
            self.current_id = id_
            # we can't know where to put it without the type, just store the reference for now
            self.variables[id_] = Variable(None, None)

    def set_type(self, type_, memory: Scheduler):
        """ Sets current var type """
        enum_value = ValueType(type_)
        address, error = memory.schedule_address(enum_value)
        if error:  # TODO Create class to create compilation errors
            return

        self.current_variable.type_ = enum_value
        self.current_variable.address_ = address

    def display(self, id_):
        print("-" * 30)
        print(f"{id_} VARS TABLE")
        print("-" * 30)
        print('{:10} {:10} {:10}'.format('ID', 'TYPE', 'DIR'))
        print("-" * 30)
        for id_, var in self.variables.items():
            # Unwrap optional. If var type is None use 'Undefined'
            type_ = 'Undefined' if var.type_.value is None else var.type_.value

            print('{:10} {:10} {:10}'.format(id_, type_, str(var.address_)))
        print("-" * 30)
