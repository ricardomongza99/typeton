from .variable_table import VariableTable


# NOTE: `type` is a reserved words in python, so
# we use the underscore at the end convention `type_`
from ..virtual.types import ValueType


class Function:
    def __init__(self, id_: str, type_="Void"):
        self.id_ = id_
        self.type_: ValueType = ValueType(type_)
        self.vars_table: VariableTable = VariableTable()

    def set_type(self, type_):
        self.type_: ValueType = ValueType(type_)
