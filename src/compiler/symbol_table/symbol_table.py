from src.compiler.symbol_table.function_table import FunctionTable
from src.utils.observer import Publisher
from .class_table import ClassTable
from .constant_table import ConstantTable
from .function_table.variable_table import VariableTable
from .global_table import GlobalTable


class SymbolTable(Publisher):
    def __init__(self):
        super().__init__()
        self.class_table = ClassTable()

        self.function_table = FunctionTable(self.class_table)
        self.constant_table = ConstantTable()
    #     self.function_table: FunctionTable = None
    #     self.variable_table: VariableTable = None
    #
    #     self.constant_table = ConstantTable()
    #     self.global_table = FunctionTable()
    #     self.class_table = ClassTable()
    #
    #     # init global
    #     self.function_table = self.global_table.functions
    #
    # def add_class(self):
    #     current = self.class_table.current_class
    #     self.variable_table = current.variables
    #     self.function_table = current.functions
    #
    # def end_class(self):
    #     self.function_table = self.global_table.functions
