from typing import Dict

from src.compiler.symbol_table.function_table.function import Function
from src.compiler.symbol_table.function_table.variable_table.variable import Variable


class GlobalTable:
    def __init__(self):
        self.variables: Dict[str, Variable] = {}
        self.functions = Dict[str, Function] = {}




