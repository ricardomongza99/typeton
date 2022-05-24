from .function_table import FunctionTable
from .constant_table import ConstantTable


class SymbolTable:
    def __init__(self):
        self.function_table = FunctionTable()
        self.constant_table = ConstantTable()
