from .variable_table import VariableTable


# NOTE: `type` is a reserved words in python, so
# we use the underscore at the end convention `type_`

class Function:
    def __init__(self, type_):
        self.type_ = type_
        self.vars_table = VariableTable()
