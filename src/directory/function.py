from .variable_table import VariableTable

# NOTE: `type` is a reserved words in python, so
# we use the underscore at the end convention `type_`
from ..virtual.types import ValueType


class Function:
    def __init__(self, id_: str):
        self.id_ = id_
        self.type_: ValueType = ValueType.VOID
        self.vars_table: VariableTable = VariableTable()
        self.has_return = False
        self.pending_type = True

    def is_pending_type(self):
        return self.pending_type

    def set_type(self, type_):
        self.pending_type = False
        self.type_: ValueType = ValueType(type_)

    def valid_function(self):
        valid_void = self.type_ is ValueType.VOID and not self.has_return
        valid_return = self.type_ is not ValueType.VOID and self.has_return
        return (valid_return and not valid_void) or (valid_void and not valid_return)
