from .variable_table import VariableTable

# NOTE: `type` is a reserved words in python, so
# we use the underscore at the end convention `type_`
from src.compiler.stack_allocator.types import ValueType


class Function:
    def __init__(self, id_: str):
        self.id_ = id_
        self.type_: ValueType = ValueType.VOID
        self._vars_table: VariableTable = VariableTable()
        self.has_return = False
        self._pending_type = True

    @property
    def variables(self):
        return self._vars_table.variables

    @property
    def current_variable(self):
        return self._vars_table.current_variable

    @property
    def vars_table(self):
        return self._vars_table

    def add_variable(self, id_, is_param):
        return self._vars_table.add(id_, is_param)

    def add_dimension(self, size):
        self._vars_table.add_dimension(size)

    def allocate_dimensions(self, layer, memory, constant_table):
        return self._vars_table.allocate_dimensions(layer, memory, constant_table)

    def set_variable_type(self, type_, layer, memory, class_id):
        return self._vars_table.set_type(type_, layer, memory, class_id)

    def display_variables(self, id_):
        self._vars_table.display(id_)

    def is_pending_type(self):
        return self._pending_type

    def set_type(self, type_):
        self._pending_type = False
        self.type_: ValueType = ValueType(type_)

    def valid_function(self):
        valid_void = self.type_ is ValueType.VOID and not self.has_return
        valid_return = self.type_ is not ValueType.VOID and self.has_return
        return (valid_return and not valid_void) or (valid_void and not valid_return)
