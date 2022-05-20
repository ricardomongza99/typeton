from .variable_table import VariableTable


# NOTE: `type` is a reserved words in python, so
# we use the underscore at the end convention `type_`
from ..virtual.types import ValueType


class Function:
    def __init__(self, id_: str, type_="Void", type_pending: bool = False):
        self.id_ = id_
        self.has_return_value = False
        self.type_: ValueType = ValueType(type_)
        self.type_pending = type_pending
        self.vars_table: VariableTable = VariableTable()

    def set_type(self, type_):
        self.type_: ValueType = ValueType(type_)

    def is_valid(self):
        if self.type_ != ValueType.VOID and self.has_return_value:
            variables = self.vars_table.variables
            for key in variables:
                variable = variables[key]
                if variable.isReturned:
                    return True
            return False
        return True
